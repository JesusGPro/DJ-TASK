from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Price(models.Model):
    code = models.CharField(max_length=16, unique=True)
    denomination = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[
        ('EUR', 'Euros'),
        ('USD', 'Dollars'),
        ('SAR', 'SAR')
    ])
    tag = models.CharField(max_length=10, choices=[
        ('task', 'Task'),
        ('manpower', 'Manpower'),
        ('material', 'Material'),
        ('machinery', 'Machinery'),
        ('canon', 'Canon'),
        ('service', 'Service'),
        ('other', 'Other')
    ])
    reference = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.denomination}"
    

class TaskSelection(models.Model):
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=3)
    drawer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    drawer_object_id = models.PositiveIntegerField()
    drawer = GenericForeignKey('drawer_content_type', 'drawer_object_id')

    def __str__(self):
        return f"{self.price.code} - {self.quantity} {self.price.currency}"
    
class TaskGroup(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class TaskSubGroup(models.Model):
    name = models.CharField(max_length=255)
    parent_group = models.ForeignKey('TaskGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=255)
    subgroup = models.ForeignKey(TaskSubGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TaskInstance(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # e.g., "Mined Tunnel in chainage 3+300"
    attributes = models.TextField(blank=True, null=True)  # e.g., {"chainage": "3+300", "other_attribute": "value"}

    def __str__(self):
        return self.name
    
    def get_all_groups(self):
        return self.task.get_all_groups()
    
####################################################################################################3

class TaskSelectionQuantity(models.Model):
    task = models.ForeignKey('TaskSelection', on_delete=models.CASCADE)
    denomination = models.CharField(max_length=255, blank=True, null=True)
    nr = models.DecimalField(max_digits=30, decimal_places=3)
    width = models.DecimalField(max_digits=30, decimal_places=3)
    length = models.DecimalField(max_digits=30, decimal_places=3)
    height = models.DecimalField(max_digits=30, decimal_places=3)
    quantity = models.DecimalField(max_digits=30, decimal_places=3)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Task Selection Quantity for {self.task}"