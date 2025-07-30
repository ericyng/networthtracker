from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    return value.split(arg)

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key"""
    return dictionary.get(key)

@register.filter
def get_balance(entry):
    """Get balance from an account entry"""
    if entry and hasattr(entry, 'balance'):
        return entry.balance
    return 0.00

@register.filter
def get_notes(entry):
    """Get notes from an account entry"""
    if entry and hasattr(entry, 'notes'):
        return entry.notes
    return '' 