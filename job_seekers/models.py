from django.db import models
from django.contrib.auth.models import User

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    resume = models.FileField(upload_to='job_seekers/resumes/', null=True, blank=True)
    skills = models.TextField()
    address = models.TextField() 
    country = models.CharField(max_length=50)
    about = models.CharField(max_length=600)
    education = models.CharField(max_length=600)
    experiences = models.CharField(max_length=600)

    def __str__(self):
        return self.user.username
