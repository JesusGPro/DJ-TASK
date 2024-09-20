from django import template
from decimal import Decimal
register = template.Library()

@register.simple_tag
def if_logged_in(user, project):
    if user.is_authenticated:
        return 'Create Price'
    else:
        return ''
    

@register.simple_tag
def multiply(unit, quantity):
        unit = float(unit)
        quantity = float(quantity)
        total_quantity = round(unit * quantity, 2)
        return str(total_quantity)

