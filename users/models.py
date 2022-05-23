from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    """ Custom User Model"""
    
    GENDER_MALE = 'male'
    GENDER_FEMAIL = 'female'
    GENDER_OTHER = 'other'

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMAIL, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True)
    bio = models.TextField(default="")