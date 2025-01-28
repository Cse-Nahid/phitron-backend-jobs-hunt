
from django.contrib import admin
from .models import ContactUs

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')  # Fixed fields

admin.site.register(ContactUs, ContactModelAdmin)