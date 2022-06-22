from accounts.models import Transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


@receiver(pre_save, sender=Transaction)
def update_transaction(sender, instance, **kwargs):
    transaction = instance
    try:
        price = transaction.order.price
        transaction.amount = price
    except:
        pass


@receiver(pre_save, sender=Transaction)
def create_transaction(sender, instance, **kwargs):
    transaction = instance
    customer = instance.customer
    try:
        pre_transaction = Transaction.objects.get(id=transaction.id)
    except:
        pre_transaction = None
    if transaction.type == 'deposit':
        if pre_transaction:
            transaction.account.wallet -= pre_transaction.amount
        transaction.account.wallet += transaction.amount
        if customer:
            if pre_transaction:
                customer.totalSpend -= pre_transaction.amount
            customer.totalSpend += transaction.amount
            customer.save()
    elif transaction.type == 'expense':
        if pre_transaction:
            transaction.account.wallet += pre_transaction.amount
        transaction.account.wallet -= transaction.amount
        if customer:
            if pre_transaction:
                customer.totalSpend += pre_transaction.amount
            customer.totalSpend -= transaction.amount
            customer.save()
    transaction.account.save()


@receiver(pre_delete, sender=Transaction)
def delete_transaction(sender, instance, **kwargs):
    transaction = instance
    customer = instance.customer
    if transaction.type == 'deposit':
        transaction.account.wallet -= transaction.amount
        if customer:
            customer.totalSpend -= transaction.amount
            customer.save()
    elif transaction.type == 'expense':
        transaction.account.wallet += transaction.amount
        if customer:
            customer.totalSpend += transaction.amount
            customer.save()
    transaction.account.save()
