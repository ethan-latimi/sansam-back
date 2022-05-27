from django.db import models

from core.models import TimeStampedModel


class Todo(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="memo")
    content = models.CharField(max_length=1024, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
