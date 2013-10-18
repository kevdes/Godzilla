from authoring.models import AssetReport
from django.contrib.auth.models import User
from django.db.models import Q

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse

from datetime import datetime
import re
import cgi

FROM_EMAIL = 'aus.dvd.authoring@bydeluxe.com)'
SUBJECT_PREFIX = '[godzilla] '

WEBSITE_ADDRESS = "http://127.0.0.1:8000/"

HTML_CSS = ' <style type="text/css">'
HTML_CSS += 'body {background-color: #666666;}'
HTML_CSS += 'body,td,th {font-family: Arial, Helvetica, '
HTML_CSS += 'sans-serif;	font-size: 12px;}'
HTML_CSS += 'p { margin-top: 0%; margin-bottom: 10px; }'
HTML_CSS += '</style>'

def send_QA_report(report_id):
	reportInfo = getReportInfo(report_id)
	reportInfo['email_list'].append('aus.dvd.authoring@bydeluxe.com')

	text_msg  = text_msg_intro(reportInfo, 'QA REPORT')
	text_msg += text_msg_items(reportInfo, False)
	text_msg += text_msg_outro(reportInfo)


	html_msg = html_msg_intro(reportInfo, 'QA REPORT')
	html_msg += html_web_link(reportInfo, True)

	# html_msg += '<p><b>Notes:</b>' + reportInfo['qa_notes'] + '</p>\n'

	html_msg += html_msg_items(reportInfo, False)
	html_msg += html_msg_outro(reportInfo, True)


	text_content = text_msg
	html_content = html_msg
	subject = 'QA Report Complete: ' + reportInfo['title'] + ' ' + reportInfo['description'] + ' ' + reportInfo['product_type'] + ' / ' + reportInfo['asset_name']

	send_email(subject, reportInfo['email_list'], text_content, html_content)

	return reportInfo['email_list']


def send_QA_response(report_id):
	reportInfo = getReportInfo(report_id)
	reportInfo['email_list'].append('aus.dvd.authoring@bydeluxe.com')
	#reportInfo['email_list'].append('aus.ms.cer@bydeluxe.com')

	text_msg  = text_msg_intro(reportInfo, 'QA AUTHOR RESPONSE')
	text_msg += text_msg_items(reportInfo, True)
	text_msg += text_msg_outro(reportInfo)


	html_msg = html_msg_intro(reportInfo, 'QA AUTHOR RESPONSE')
	html_msg += html_web_link(reportInfo, False)
	
	html_msg += html_asset_status(reportInfo)
	# html_msg += '<p><b>Notes:</b>' + reportInfo['qa_notes'] + '</p>\n'

	html_msg += html_msg_items(reportInfo, True)

	html_msg += html_asset_status(reportInfo)
	
	html_msg += html_msg_outro(reportInfo, False)


	text_content = text_msg
	html_content = html_msg
	subject = 'QA Author Response: ' + reportInfo['title'] + ' ' + reportInfo['description'] + ' ' + reportInfo['product_type'] + ' / ' + reportInfo['asset_name']

	send_email(subject, reportInfo['email_list'], text_content, html_content)

	return reportInfo['email_list']

def text_msg_intro(reportInfo, subject):

	text_msg = reportInfo['product_type'] + ' ' + subject +'\n\n'
	text_msg += '-----------------\n\n'
	text_msg += reportInfo['title'] + ' ' + reportInfo['description'] + ' ' + reportInfo['product_type'] + '\n'
	text_msg += reportInfo['asset_name'] + '\n\n'

	text_msg += 'QA REQUEST:\n'
	text_msg += '---------------\n\n'
	text_msg += 'QA Disc #' + reportInfo['qa_disc'] + ' / ' + 'Work Order #' + reportInfo['work_order'] + '\n'
	text_msg += 'Created by: ' + reportInfo['created_by'] + '\n\n'
	#text_msg += 'QA Notes: \n'
	#text_msg += reportInfo['qa_notes'] + '\n\n'

	return text_msg

def text_msg_items(reportInfo, showResponse):
	num_items = 1

	text_msg = 'QA REPORT:\n'
	text_msg += '---------------\n\n'

	for item in reportInfo['assetReportItems']:
	#	text_msg += 'Item #' + str(num_items) + '\n'
		text_msg += 'Submitted by: ' + str(item.cer_user) + '\n'
		text_msg += 'Severity: ' + str(item.severity) + '\n'
		text_msg += 'Comment: ' + str(item.comment.encode("utf8")) + '\n\n'

		if showResponse:
			text_msg += 'AUTHOR RESPONSE:\n'
			text_msg += 'Submitted by: ' + str(item.response_user) + '\n'
			text_msg += 'Status: ' + str(item.response_status) + '\n'
			text_msg += 'Comment: ' + str(item.response_comment.encode("utf8")) + '\n\n'

		num_items += 1

	return text_msg

def text_msg_outro(reportInfo):
	text_msg = 'Go to ' 
	text_msg += WEBSITE_ADDRESS + reverse('asset-detail', kwargs={'product_id': reportInfo['product_id'], 'asset_id': reportInfo['asset_id']})+'#'+ str(reportInfo['report_id']) + ' '
	text_msg += 'to view report.\n\n'

	return text_msg


def html_msg_intro(reportInfo, subject):
	html_msg = '<html>'
	html_msg += HTML_CSS
	html_msg += '<body bgcolor="#666666" style="background-color:#666666;font-family:Arial, sans-serif;font-size:12px;" >\n'

	html_msg += '<table width="600" border="0" align="center" cellpadding="14" bgcolor="#FFFFFF">\n'
	html_msg += '<tr valign="middle">\n'
	html_msg += '    <td valign="top">\n'
	html_msg += '		<p style="font-size: 11px; color: #666666;">\n'
	html_msg += 		reportInfo['product_type'].upper() + ' ' + subject + '\n'
	html_msg += '			 </p>\n'
	html_msg += '	    <p style="font-size: 20px; color: #009900; font-weight: bold;">\n'
	html_msg += 	    reportInfo['title'] + ' ' + reportInfo['description'] + ' ' + reportInfo['product_type'] + '</p>\n'
	html_msg += '    	<p style="color: #666666; font-size: 18px; font-weight: bold;">\n'
	html_msg += 		reportInfo['asset_name'] + '\n'
	html_msg += '	    </p>\n'
	html_msg += '	    <table width="100%" border="0" cellpadding="6" cellspacing="0" \n'
	html_msg += '	     bordercolor="#006600" style="border-width: 1px; \n'
	html_msg += '	     border-style: solid; border-color: #006600;">\n'
	html_msg += '          <tr bgcolor="#006600">\n'
	html_msg += '            <td colspan="2"><span style="color: #FFFFFF; font-weight: bold;">QA REQUEST </span></td>\n'
	html_msg += '          </tr>\n'
	html_msg += '          <tr>\n'
	html_msg += '            <td width="90"><strong>Created by: </strong></td>\n'
	html_msg += '            <td>' + reportInfo['created_by'] + '</td>\n'
	html_msg += '          </tr>\n'
	html_msg += '          <tr>\n'
	html_msg += '            <td width="90"><strong>QA Disc:</strong></td>\n'
	html_msg += '            <td>' + reportInfo['qa_disc'].zfill(3) + '</td>\n'
	html_msg += '          </tr>\n'
	html_msg += '          <tr>\n'
	html_msg += '            <td width="90"><strong>Work Order:</strong></td>\n'
	html_msg += '            <td>' + reportInfo['work_order'] + '</td>\n'
	html_msg += '          </tr>\n'
	html_msg += '        </table>\n'
	html_msg += '		<p>&nbsp;</p>\n'

	return html_msg

def html_web_link(reportInfo, canRespond):

	html_msg = '		<p><a href="' + WEBSITE_ADDRESS + reverse('asset-detail', kwargs={'product_id': reportInfo['product_id'], 'asset_id': reportInfo['asset_id']})+'#'+ str(reportInfo['report_id']) + '">Click here</a>\n'
	if canRespond:
		html_msg += ' 		to view and respond to report.</p>\n' 
	else:
		html_msg += ' 		to view report.</p>\n' 

	return html_msg

def html_msg_outro(reportInfo, canRespond):

	#html_msg = '	</td>\n'
	html_msg = '<p>&nbsp;</p>\n'

	html_msg += html_web_link(reportInfo, canRespond)

	html_msg += '	</tr>\n'
	html_msg += '</table>\n'

	html_msg += '<small>\n'
	return html_msg


def html_msg_items(reportInfo, showResponse):
	html_msg = '<p>&nbsp;</p>\n'
	html_msg += '<table width="100%" border="0" cellpadding="6" cellspacing="0" bordercolor="#009900" \n'
	html_msg += ' style="border-width: 1px; border-style: solid; border-color: #009900;">\n'
	html_msg += '		<tr>\n'
	html_msg += '		<td bgcolor="#009900" style="padding: 6px"><span style="color: #FFFFFF; \n'
	html_msg += ' font-weight: bold;"> QA REPORT </span></td>\n'
	html_msg += '		</tr>\n'
	html_msg += '		<tr>\n'
	html_msg += '		    <td><table width="100%" border="0" cellpadding="6" \n'
	html_msg += ' cellspacing="0" bgcolor="#FFFFFF">\n'

	num_items = 1
	for item in reportInfo['assetReportItems']:


		html_msg += '		<tr style="border-width: 1px; border-style: solid; border-color: #CCCCCC;">\n'
		html_msg += '		    <td width="85" align="center" valign="top" style="border-top-width: 1px;\n'
		html_msg += '		    border-bottom-width: 1px; border-left-width: 1px; border-top-style: solid;\n'
		html_msg += '		border-bottom-style: solid;	border-left-style: solid; border-color: #ECECEC;">\n'
		html_msg += '		<p><strong>Severity:</strong><br />\n'
		
		if str(item.severity) == 'High':
			html_msg += '		       <span style="color: #FF0000; font-weight: bold;">\n'
		elif str(item.severity) == 'Medium':
			html_msg += '		       <span style="color: #FF6600; font-weight: bold;">\n'
		elif str(item.severity) == 'Low':
			html_msg += '		       <span style="color: #009933; font-weight: bold;">\n'
		else:
			html_msg += '<span>\n'

		html_msg += 				str(item.severity) + '\n'
		html_msg += '				</span><br />\n'
		html_msg += '		       <div style="font-size: 10px; margin-top: 8px;">\n'
		html_msg += '		       <p style="color: #999999;"> Submitted by:<br />\n'
		html_msg += '		       <span style="color: #000000;">' + str(item.cer_user) + '</span></p>\n'
		html_msg += '			  </div></td>\n'
		html_msg += '		    <td valign="top" style="border-width: 1px; border-style: solid; border-color: #ECECEC; \n'
		#html_msg += ' border-top-width: 1px; border-top-style: solid; border-top-color: #CCCCCC; \n'
		#html_msg += ' border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #CCCCCC; \n'
		html_msg += ' margin-bottom: 10px">\n'		
		html_msg += '		  <p>\n'
		html_msg += 		  format_html_comments(item.comment) + '\n'
		html_msg += '		 </p></td>\n'
		html_msg += '		 </tr>\n'

		if showResponse:
			html_msg += '		 <tr bgcolor="#E0E0E0">\n'
			html_msg += '		 <td align="center" valign="top" bgcolor="#E0E0E0"><p><strong>Status:</strong><br />\n'

			if str(item.response_status) == 'To be fixed':
				html_msg += '		       <span style="color: #FF0000; font-weight: bold;">\n'
			elif str(item.response_status) == 'Fixed - retest required':
				html_msg += '		       <span style="color: #FF6600; font-weight: bold;">\n'
			elif str(item.response_status) == 'Acceptable' or str(item.response_status) == 'Pass' or str(item.response_status) == 'Fixed - author approved':
				html_msg += '		       <span style="color: #009933; font-weight: bold;">\n'
			else:
				html_msg += '<span>\n'

			html_msg += 			str(item.response_status) + '</span><br />\n'
			html_msg += '		 <div style="font-size: 10px; margin-top: 8px;">\n'
			html_msg += '		 <p style="color: #666666;"> Submitted by:<br />\n'
			html_msg += '		 <span style="color: #000000;">' + str(item.response_user.first_name) + ' ' + str(item.response_user.last_name) + '</span></p>\n'
			html_msg += '		 </div></td>\n'
			html_msg += '		 <td valign="top" style="border-left-width: 1px;\n'
			html_msg += '		 border-left-style: solid; border-left-color: #FFFFFF;">\n'
			html_msg += '		 <p><strong>Author response:</strong></p>\n'
			html_msg += '		 ' + format_html_comments(item.response_comment) + '\n'
			html_msg += '		 </td>\n'
			html_msg += '		 </tr>\n'


		html_msg += '		 <tr>\n'
		html_msg += '		     <td height="4" colspan="2"></td>\n'
		html_msg += '		 </tr>\n'

		num_items += 1

	html_msg += '	</table>\n'

	html_msg += '	</td>\n'
	html_msg += '	</tr>\n'
	html_msg += '		</table>\n'
	html_msg += '<p>&nbsp;</p>\n'
	return html_msg

def format_html_comments(comments):
	comments = cgi.escape(comments).encode('ascii', 'xmlcharrefreplace')
	html_comments = re.compile(r'(((\d+:\d+:\d+)|(\d+.\d+.\d+)|(\d+:\d+)|(\d+.\d+)\s*?)+)', re.I).sub(r'<b>\1</b>', comments)
	html_comments = html_comments.replace('\n', '<br />\n')
	return html_comments

def html_asset_status(reportInfo):
	html_msg = '	<table width="100%" border="0" cellpadding="6" cellspacing="0">\n'
	html_msg += '		<tr>\n'
	if reportInfo['asset_status'] == 'Author Approved':
		html_msg += '		<td align="center" bgcolor="#009900"><span style="color: #FFFFFF"><strong>ASSET STATUS: </strong>PASS</span></td>\n'
	else:
		html_msg += '		<td align="center" bgcolor="#CC0000"><span style="color: #FFFFFF"><strong>ASSET STATUS: </strong>FAIL</span></td>\n'
	html_msg += '		</tr>\n'
	html_msg += '		</table>\n'

	return html_msg

def getReportInfo(report_id):
	reportInfo = {}
	
	assetReport = AssetReport.objects.get(pk=report_id)
	email_list = list(User.objects.values_list('email', flat=True).filter(Q(groups__name='authoring') | Q(groups__name='management') & ~Q(email='')).distinct())

	assetReportItems = assetReport.reportitem_set.all().order_by('date_created')

	
	reportInfo['report_id'] = report_id
	reportInfo['email_list'] = email_list
	reportInfo['assetReportItems'] = assetReportItems

	reportInfo['product_id'] = assetReport.asset.product.id
	reportInfo['asset_id']= assetReport.asset.id
	reportInfo['asset_status'] = str(assetReport.asset.status)

	reportInfo['title'] = str(assetReport.asset.product.title)
	reportInfo['description'] = str(assetReport.asset.product.name)
	reportInfo['product_type']= str(assetReport.asset.product.product_type)

	reportInfo['asset_name'] = str(assetReport.asset.name)

	reportInfo['qa_disc'] = str(assetReport.disc_number)
	reportInfo['work_order'] = str(assetReport.work_order)

	reportInfo['created_by'] = str(assetReport.created_by)
	reportInfo['created_date'] = assetReport.date_created.strftime('%a, %b %d, %I:%M%p')

	reportInfo['qa_notes'] = str(assetReport.contents)

	return reportInfo

def send_email(subject, to_email, text_msg, html_msg, from_email=FROM_EMAIL):

	subject = SUBJECT_PREFIX + subject

	msg = EmailMultiAlternatives(subject, text_msg, from_email, to_email)
	msg.attach_alternative(html_msg, "text/html")
	msg.send()