from operator import mod
from django.db import models

# Create your models here.
class user(models.Model):
    fullname=models.CharField(max_length=150, null=True, blank=False)
    username=models.CharField(max_length=30, null=False, blank=False, unique=True)
    email=models.CharField(max_length=60, null=False, blank=False)
    password=models.CharField(max_length=55, null=False, blank=False)




