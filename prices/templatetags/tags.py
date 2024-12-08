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
    

@register.filter
def get_letter(letters, index):
    if index > 25:
        return 'N/A'
    else: 
        return letters[index]

   
   

@register.filter
def get_first_part(string, int):
    string_list = []
    for s in string[:int]:
        string_list.append(s)
    first_part = ''.join(string_list)
    return first_part

@register.filter
def get_second_part(string, int):
    string_list = []
    for s in string[int:]:
        string_list.append(s)
    second_part = ''.join(string_list)
    return second_part

@register.filter
def get_second_value(value):
    if isinstance(value, tuple) and len(value) > 1:
        return value[1]
    return None  

@register.filter
def get_first_value(value):
    if isinstance(value, tuple) and len(value) > 1:
        return value[0]
    return None  


@register.filter
def get_first_part_upper(string, int):
    string_list = [s.upper() for s in string[:int]]
    
    first_part = ''.join(string_list)
    return first_part
    



