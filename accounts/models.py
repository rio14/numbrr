from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

class Userprofile(models.Model):
    owner = models.CharField(max_length=255)
    useraname = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.IntegerField()
    area = models.TextField()
    senderid = models.CharField(max_length=6)
