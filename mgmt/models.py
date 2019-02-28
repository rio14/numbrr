from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    owner = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    mobile = models.IntegerField(blank=False)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    subarea = models.CharField(max_length=100)
    anniversary = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Staff(models.Model):
    owner = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    mobile = models.IntegerField(blank=False)
    area = models.CharField(max_length=100)
