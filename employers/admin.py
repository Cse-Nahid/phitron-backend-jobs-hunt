from django.contrib import admin
from .models import EmployerProfile


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_description')
    search_fields = ('company_name',)
