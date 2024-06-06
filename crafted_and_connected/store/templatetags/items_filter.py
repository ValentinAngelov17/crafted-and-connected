from django import template

register = template.Library()

@register.filter
def split(value):
    if value:
        return value.split(", ")
    return []