from django import template
register = template.Library()

@register.filter(name='choiceval')
def choiceval(boundfield, value):
	return list(boundfield.field.choices)[value][1]
	#return dict(boundfield.field.choices).get(boundfield.value)
    #return dict(boundfield.field.choices)[form.data[field_name]]