from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Lookup a value in a dictionary by key"""
    return dictionary.get(key, [])
