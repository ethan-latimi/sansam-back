from django.contrib import admin
from . import models


@admin.register(models.Farm)
class FarmAdmin(admin.ModelAdmin):

    """ Customized Farm Admin """

    list_display = (
        "title",
        "introduction",
        "logs"
    )

    def logs(self, obj):
        return obj.logs.count()


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):

    """ Customized Log Admin """

    list_display = (
        'title',
        'farm',
    )
