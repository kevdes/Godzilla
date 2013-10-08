import win32com.client.dynamic, sys, re
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
			if self.MAPIProfile <> None: 
				MAPIProfile = self.MAPIProfile 
			else: 
				MAPIProfile = "" 				
			mapi = win32com.client.dynamic.Dispatch("MAPI.session")
			mapi.Logon('Deluxe')


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


	def _send(self, email_message): 
		"""A helper method that does the actual sending.""" 
		if not email_message.recipients(): 
			return False 
		recipients = map(self._sanitize, email_message.recipients()) 
		Msg = o.CreateItem(0)
 		Msg.To = recipients
		Msg.Subject = 'subject'
		Msg.Body = 'text'
		self.connection.SaveChanges(0)

		Msg.Send()
		return True 








