from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    """ Time Staemped Model """

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
