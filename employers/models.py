from django.db import models
from django.contrib.auth.models import User


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,default="")
    last_name = models.CharField(max_length=100,default="")
    company_name = models.CharField(max_length=255,default="")
    company_description = models.TextField()
    company_website = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.company_name
