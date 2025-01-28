from django.contrib import admin
from .models import JobSeekerProfile

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume', 'skills')
    search_fields = ('user__username',)
