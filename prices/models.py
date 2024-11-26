from django.db import models
from tasks.models import Project
from django.contrib.auth.models import User

class Price(models.Model):
    code = models.CharField(max_length=20, unique=True)
    denomination = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=20, choices=[
        ('EUR', 'Euros'),
        ('USD', 'Dollars'),
        ('SAR', 'SAR'),
        ('No currency', 'No currency'),
    ])
    unit = models.CharField(max_length=5, default="nr")
    tag = models.CharField(max_length=30, choices=[
        ('work', 'Work'),
        ('manpower', 'Manpower'),
        ('material', 'Material'),
        ('machinery', 'Machinery'),
        ('canon', 'Canon'),
        ('subcontract', 'Subcontract'),
        ('other', 'Other'),
        ('overhead', 'Overhead'),
    ])
    reference = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.code}"
    

class Task(models.Model):
    code = models.CharField(max_length=20, default="LNNN.NNN", unique=True)
    name = models.CharField(max_length=255)
    project = models.ForeignKey('tasks.Project', on_delete=models.CASCADE)
    unit = models.CharField(max_length=5)  # e.g., m3, etc.
    price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=20, choices=[
        ('EUR', 'Euros'),
        ('USD', 'Dollars'),
        ('SAR', 'SAR'),
        ('No currency', 'No currency'),

    ])
    components = models.ManyToManyField('Price', through='TaskComponent')
    
    

class TaskComponent(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    code = models.ForeignKey(Price, on_delete=models.CASCADE, validators=[])
    quantity = models.DecimalField(max_digits=30, decimal_places=6)
    
    
