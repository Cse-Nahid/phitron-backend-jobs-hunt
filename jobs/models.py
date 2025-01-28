from django.db import models
from django.conf import settings  # Import settings to reference the custom user model

class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Correctly reference the custom user model here
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    date_posted = models.DateField(auto_now_add=True)
    category = models.ForeignKey('JobCategory', on_delete=models.CASCADE, related_name='jobs')
    company_name = models.CharField(max_length=30)
    experience = models.CharField(max_length=255)
    employee_type = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    offer_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    responsibilities = models.TextField()
    qualifications = models.TextField()
    skills_experience = models.TextField()

    def __str__(self):
        return self.title

class JobCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
