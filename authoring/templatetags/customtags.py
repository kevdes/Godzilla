from django import template
from django.template.defaultfilters import stringfilter
import re
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter(name='choiceval')
def choiceval(boundfield, value):
	return list(boundfield.field.choices)[value][1]
	#return dict(boundfield.field.choices).get(boundfield.value)
	#return dict(boundfield.field.choices)[form.data[field_name]]

@register.simple_tag(name='bold_timecode')
@stringfilter
def bold_timecode(comments):
	html_output = re.compile(r'(((\d+:\d+:\d+)|(\d+.\d+.\d+)|(\d+:\d+)|(\d+.\d+)\s*?)+)', re.I).sub(r'<b>\1</b>', comments)
	return html_output

@register.simple_tag(name='bold_headings')
@stringfilter
def bold_headings(text):
	full_text = text.split('\n') 
	html_text = []
	for each_line in full_text:
		if not each_line == '':
			split_line = each_line.split(':', 1)	
			html_text.append('<b>' + split_line[0] + ':</b>'  + split_line[1] + '<br />')

		else:
			html_text.append('<br />')
	
	return ''.join(html_text)

@register.simple_tag(name='split_directory')
@stringfilter
def split_directory(directory, dir_listing=True):
	split_dir = directory.split('\\')

	prog_dir = ''
	compiled_dir = ''

	for index, part_dir in enumerate(split_dir):
		if index == len(split_dir)-1 and dir_listing:
			compiled_dir += '<span class="gray">' + part_dir + '</span> \\ '
		else:
			compiled_dir += '<a href="' + reverse('show_dir') + '?path=' + prog_dir + part_dir + '">' + part_dir + ' </a> \\ '
		prog_dir += part_dir + '\\'

	return compiled_dir


@register.filter(name='fix_amper')
def fix_amper(string):
	return string.replace('&', '%26')