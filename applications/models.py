from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/resumes/',blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.job_seeker.username}"
