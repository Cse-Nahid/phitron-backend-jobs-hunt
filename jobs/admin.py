from django.contrib import admin
from .models import Job, JobCategory

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'date_posted', 'experience', 'offer_salary')
    search_fields = ('title', 'employer__username')

admin.site.register(Job, JobAdmin)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)