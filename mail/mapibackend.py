from win32com.mapi import mapi 
from win32com.mapi import mapitags 
import threading 

from django.conf import settings 
from django.core.mail.backends.base import BaseEmailBackend 

class EmailBackend(BaseEmailBackend): 
	""" 
	A wrapper that manages the MAPI interface. 
	""" 
	def __init__(self, MAPIProfile=None, fail_silently=False, **kwargs): 
		super(EmailBackend, self).__init__(fail_silently=fail_silently) 
		self.MAPIProfile = MAPIProfile or settings.EMAIL_MAPIPROFILE
		self.connection = None 
		self._lock = threading.RLock() 

	def open(self): 
		""" 
		Ensures we have a MAPI Session to the exchange server. Returns whether or 
		not a new connection was required (True or False). 
		""" 
		if self.connection: 
			# Nothing to do if the connection is already open. 
			return False 
		try: 			
			mapi.MAPIInitialize(None) 
			if self.MAPIProfile <> None: 
				MAPIProfile = self.MAPIProfile 
			else: 
				MAPIProfile = "" 				
			session = mapi.MAPILogonEx(0, MAPIProfile, None, mapi.MAPI_EXTENDED | mapi.MAPI_USE_DEFAULT) 
			messagestorestable = session.GetMsgStoresTable(0) 
			messagestorestable.SetColumns((mapitags.PR_ENTRYID, mapitags.PR_DISPLAY_NAME_A, mapitags.PR_DEFAULT_STORE),0) 
			while True: 
				rows = messagestorestable.QueryRows(1, 0) 
				#if this is the last row then stop 
				if len(rows) != 1: 
					break 
				row = rows[0] 
				#if this is the default store then stop 
				if ((mapitags.PR_DEFAULT_STORE,True) in row): 
					break		 
			# unpack the row and open the message store 
			(eid_tag, eid), (name_tag, name), (def_store_tag, def_store) = row 
			msgstore = session.OpenMsgStore(0,eid,None,mapi.MDB_NO_DIALOG | mapi.MAPI_BEST_ACCESS) 
			# get the outbox 
			hr, props = msgstore.GetProps((mapitags.PR_IPM_OUTBOX_ENTRYID), 0) 
			(tag, eid) = props[0] 
			#check for errors 
			if mapitags.PROP_TYPE(tag) == mapitags.PT_ERROR: 
				raise TypeError('got PT_ERROR instead of PT_BINARY: %s'%eid) 
			self.connection = msgstore.OpenEntry(eid,None,mapi.MAPI_BEST_ACCESS) 
			return True 
		except:
			if not self.fail_silently: 
				raise 

	def close(self): 
		"""Closes the connection to the exchange server.""" 
		self.connection = None 

	def send_messages(self, email_messages): 
		""" 
		Sends one or more EmailMessage objects and returns the number of email 
		messages sent. 
		""" 
		if not email_messages: 
			return 
		self._lock.acquire() 
		try: 
			new_conn_created = self.open() 
			if not self.connection: 
				# We failed silently on open(). 
				# Trying to send would be pointless. 
				return 

			num_sent = 0 
			for message in email_messages: 
				sent = self._send(message)
				if sent: 
					num_sent += 1 
			if new_conn_created: 
				self.close()
		finally: 
			self._lock.release() 
		return num_sent 

	def _sanitize(self, email): 
		name, domain = email.split('@', 1) 
		email = '@'.join([name, domain.encode('idna')]) 
		return email 

	def _makeentry(self, recipient, recipienttype): 
		"""A helper method that creates the MAPI Object for the recipient.""" 
		return ((mapitags.PR_RECIPIENT_TYPE, recipienttype), 
								(mapitags.PR_SEND_RICH_INFO, False), 
								(mapitags.PR_DISPLAY_TYPE, 0), 
								(mapitags.PR_OBJECT_TYPE, 6), 
								(mapitags.PR_EMAIL_ADDRESS_A, recipient), 
								(mapitags.PR_ADDRTYPE_A, 'SMTP'), 
								(mapitags.PR_DISPLAY_NAME_A, recipient)) 

	def _send(self, email_message): 
		"""A helper method that does the actual sending.""" 
		if not email_message.recipients(): 
			return False 
		recipients = map(self._sanitize, email_message.recipients()) 
		message = self.connection.CreateMessage(None,0)
		pal = [] 
		for recipient in recipients: 
			pal.extend([self._makeentry(recipient, mapi.MAPI_TO)]) 
		# add the resolved recipients to the message 
		message.ModifyRecipients(mapi.MODRECIP_ADD,pal) 
 
		message.SetProps([(mapitags.PR_BODY_A,email_message.body), (mapitags.PR_SUBJECT_A,email_message.subject)]) 
		self.connection.SaveChanges(0)

		message.SubmitMessage(0) 
		return True 
