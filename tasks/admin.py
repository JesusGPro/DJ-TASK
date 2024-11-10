from django.contrib import admin
from .models import Project, ActiveProject, Currency

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'currency', 'created_at', 'tenant')

@admin.register(ActiveProject)
class ActiveProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('eur_sar', 'usd_sar', 'eur_usd')


