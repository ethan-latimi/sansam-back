from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel


class Farm(TimeStampedModel):

    """ Field (밭)"""

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, default="무제")
    introduction = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
# 여러장의 사진이 필요한지 물어봐야함


class Log(TimeStampedModel):

    """ Logs (영농일지)"""

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(
        max_length=255, default=f"{timezone.now}", null=True, blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    worker = models.CharField(max_length=255, default="")
    note = models.CharField(max_length=255, default="", null=True, blank=True)
    weather = models.CharField(
        max_length=255, default="맑음", null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name='logs', null=True)

    def __str__(self):
        return f'{self.farm} - log{self.id}'
