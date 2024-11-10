from django.contrib import admin
from .models import Price, Task, TaskComponent

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('code', 'denomination', 'price', 'currency', 'tag', 'reference')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'project', 'unit', 'price', 'currency')

@admin.register(TaskComponent)
class TaskComponentAdmin(admin.ModelAdmin):
    list_display = ('task', 'code', 'quantity')
