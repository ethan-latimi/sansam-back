from django.db import models
from django.core.validators import RegexValidator

from core.models import TimeStampedModel


class Reference(models.Model):

    """ Customer's reference detail (소개자) """

    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(TimeStampedModel):

    """ Customer Model (고객)"""

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=30, null=True, blank=True)
    phoneNumberRegex = RegexValidator(regex=r"^\d{2,3}-\d{3,4}-\d{4}$")
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex], max_length=14)
    secondPhoneNumber = models.CharField(
        validators=[phoneNumberRegex], max_length=14, null=True, blank=True)
    totalSpend = models.IntegerField(default=0, blank=True)
    reference = models.CharField(max_length=200)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=True, related_name="customers")
    company = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
