from django.contrib import admin
from .models import WorkLevel, WorkPackage, Work, Measurement, WorkpackageTotals

@admin.register(WorkLevel)
class WorkLevelAdmin(admin.ModelAdmin):
    list_display = ('project', 'level_number', '__str__')

@admin.register(WorkPackage)
class WorkPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent')

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('task', 'work_package', 'quantity', 'work_amount')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('work', 'description', 'nr', 'width', 'length', 'height', 'comment', 'partial')

@admin.register(WorkpackageTotals)
class WorkpackageTotalsAdmin(admin.ModelAdmin):
    list_display = ('workpackage', 'total')
