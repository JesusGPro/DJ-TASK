import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')  # Ensure this points to your correct settings module

# Setup the Django environment
django.setup()

############## End of set up ###################################
from workpackage.models import WorkPackage, WorkpackageTotals
from collections import defaultdict
from decimal import Decimal

wps = WorkPackage.objects.all().order_by('name')
children = []
work_package_id = 34

# chose wp
work_package = WorkPackage.objects.get(id=work_package_id)

print("Work Package: ", work_package.name, work_package.description)

wp_digits = []

for digit in work_package.name:
    if digit != '0':
        wp_digits.append(digit)

prefix = ''.join(wp_digits)

for wp in wps:
    if wp.name.startswith(prefix):
        children.append(wp.name)
del children[0]

print(children)