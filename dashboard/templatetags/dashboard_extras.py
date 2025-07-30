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

@register.filter
def month_name(month_number):
    """Convert month number to month name"""
    month_names = {
        1: 'January',
        2: 'February', 
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return month_names.get(int(month_number), str(month_number)) 