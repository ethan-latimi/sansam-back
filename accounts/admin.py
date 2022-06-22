from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):

    """ Customized Account Admin """

    list_display = (
        'name',
        'owner',
        'wallet',
        'transactions',
    )

    def transactions(self, obj):
        return obj.transactions.count()


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):

    """ Customized Transaction Admin """

    list_display = (
        "amount",
        "type",
        "account",
        "order",
    )

    def transactions(self, obj):
        return obj.transactions.count()
