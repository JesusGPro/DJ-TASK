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

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 'N/A')

# @register.simple_tag
# def get_chapter_total(work_package_name, chapter_totals):
#     # Check if the work_package_name is a number followed by zeros
#     try:
#         # Convert to integer
#         number = int(work_package_name)
#         # Determine the length of the number
#         length = len(str(number))
#         # Check if it is a number followed by zeros

#         divider = 10 ** (length - 1)
#         rest = number % divider

#         if rest == 0:
#             key = str(int(number / divider))
#             return chapter_totals.get(key, 'N/A')

#         else:
#             return "It is not a chapter of subchapter"
#     except ValueError:
#         return 'N/A'  # If conversion fails, return 'N/A'

@register.simple_tag
def get_chapter_total(work_package_name, chapter_totals):
    try:
        # Determine the length of the work_package_name
        length = len(work_package_name)

        # First, check if the full work_package_name exists in chapter_totals
        if work_package_name in chapter_totals:
            return chapter_totals[work_package_name]  # Return the total for the full key

        # Iterate from 1 to length - 1 to get keys
        for i in range(1, length):  # range(1, length) gives us keys from [:1] to [:n-1]
            chapter_key = work_package_name[:i]  # Extract the substring up to i characters
            if chapter_key in chapter_totals:
                return chapter_totals[chapter_key]  # Return the total if found

        return 'N/A'  # If no valid chapter is found
    except Exception as e:
        return 'N/A'  # In case of any error, return 'N/A'


