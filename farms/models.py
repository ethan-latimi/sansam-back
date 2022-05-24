from django.db import models

from core.models import TimeStampedModel


class Farm(TimeStampedModel):

    """ Field (밭)"""

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, default="")
    introduction = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Log(TimeStampedModel):

    """ Logs (영농일지)"""

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, default="")
    content = models.CharField(max_length=500, null=True, blank=True)
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name='logs', null=True)

    def __str__(self):
        return self.title
