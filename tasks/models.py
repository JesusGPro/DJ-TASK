from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

"""
Tenant-aware model: Using a single database and table structure for all users, but add a tenant_id 
field to each model. This field identifies the user who owns the data. We can then use Django's 
built-in filtering mechanisms to restrict access to data based on the current user.
We can store all data in a single database and use Django's ORM to filter data based on the current 
user.
"""

class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    location = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ActiveProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Currency(models.Model):
    eur_sar = models.DecimalField(max_digits=10, decimal_places=2, default=4.16)
    usd_sar = models.DecimalField(max_digits=10, decimal_places=2, default=3.75)
    eur_usd = models.DecimalField(max_digits=10, decimal_places=2, default=1.11)

    def __str__(self):
        return f"EUR/SAR: {self.eur_sar}, USD/SAR: {self.usd_sar}, EUR/USD: {self.eur_usd}"



    