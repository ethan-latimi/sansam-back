from django.contrib import admin
from . import models

admin.site.register(models.Reference)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):

    """ Customized Admin """

    list_display = (
        "name",
        "address",
        "email",
        "phoneNumber",
        "totalSpend",
        "reference",
    )
