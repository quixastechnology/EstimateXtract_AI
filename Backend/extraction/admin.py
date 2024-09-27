from django.contrib import admin
from .models import Estimate

@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('pdf_file', 'created_at')
