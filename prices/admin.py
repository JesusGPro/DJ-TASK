from django.contrib import admin
from .models import Price

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('code', 'denomination', 'price', 'currency', 'tag', 'reference')
