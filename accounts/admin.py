from django.contrib import admin
from . import models

admin.site.register(models.transaction)


@admin.register(models.account)
class AccountAdmin(admin.ModelAdmin):

    """ Customized Account Admin """

    list_display = (
        'name',
        'user',
        'wallet',
        'transactions',
    )

    def transactions(self, obj):
        return obj.transactions.count()
