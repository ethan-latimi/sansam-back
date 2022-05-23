from django.db import models

from core.models import TimeStampedModel


class account(TimeStampedModel):

    """ Wallet (지갑) """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    wallet = models.IntegerField(default=0)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class transaction(TimeStampedModel):

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
    account = models.ForeignKey(account, on_delete=models.CASCADE, related_name="transactions")
    content = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type} + {self.account}"
