from django.db import models

from core.models import TimeStampedModel
from customers.models import Customer


class Account(TimeStampedModel):

    """ Wallet (지갑) """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    wallet = models.IntegerField(default=0)
    owner = models.OneToOneField(
        'users.User', on_delete=models.CASCADE, null=True, related_name="account")

    def __str__(self):
        return self.name


class Transaction(TimeStampedModel):

    """ Transaction Detail (거래 내역) """

    TRANSACTION_DEPOSIT = "deposit"
    TRANSACTION_EXPENSE = "expense"

    TRANSACTION_TYPES = (
        (TRANSACTION_DEPOSIT, 'Deposit'),
        (TRANSACTION_EXPENSE, 'Expense')
    )

    id = models.AutoField(primary_key=True, editable=False)
    amount = models.IntegerField(default=0)
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=50)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions")
    content = models.CharField(max_length=100)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="transactions")
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, null=True, blank=True, related_name="transaction")

    def __str__(self):
        return f"{self.type} + {self.account}"
