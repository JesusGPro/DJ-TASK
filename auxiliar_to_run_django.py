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

wps = WorkPackage.objects.all()
work_packages = defaultdict(list)

for wp in wps:
    print(f"Processing WorkPackage: {wp.id}, Parent ID: {wp.parent_id}")
    
    # Ensure the work package itself is in the dictionary
    work_packages[wp.name]  # This initializes the entry for every work package
    
    if wp.parent_id:
        work_packages[wp.parent.name].append(wp.name)


work_package_totals = {}

for wp in wps:
    try:
        work_package_totals[wp.name] = WorkpackageTotals.objects.get(workpackage_id=wp.id).total 

    except WorkpackageTotals.DoesNotExist:
        # If the total does not exist, set it to 0
        work_package_totals[wp.name] = 0

# Function to calculate totals recursively
def calculate_total(key):
    total = Decimal('0.00')
    # Check if the work package has child packages
    if key in work_packages:
        for child in work_packages[key]:
            total += calculate_total(child)  # Recursively sum child totals
    # Add the total for the current work package if it exists
    if key in work_package_totals:
        total += work_package_totals[key]
    return total

# Calculate totals for each chapter
chapter_totals = {}
for key in work_packages.keys():
    chapter_totals[key] = calculate_total(key)

# Print the final chapter totals
print("\nFinal Chapter Totals:")
for chapter_id, total in sorted(chapter_totals.items()):
    print(f'Chapter {chapter_id}: Total = {total:.2f}')

