from django import template
from django.template.loader import get_template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='add_attr')
def add_attr(field, attr_string):
    attrs = {}
    for attr in attr_string.split(','):
        if '=' in attr:
            key, value = attr.split('=', 1)
            attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)