from orders.models import Order, OrderItem
from accounts.models import Transaction
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    order = instance
    if created == True:
        transaction = Transaction.objects.create(
            amount=order.price,
            type="deposit",
            account=order.owner.account,
            customer=order.customer,
            order=order,
        )
    else:
        transaction = order.transaction
        transaction.save()


@receiver(pre_save, sender=Order)
def update_order(sender, instance, **kwargs):
    order = instance
    if order.receiver != '':
        order.receiver = order.customer.name
    items = OrderItem.objects.filter(order=order)
    if items != None:
        price = 0
        for i in items:
            price += i.price
        order.price = price


@receiver(post_delete, sender=Order)
def delete_order(sender, instance, **kwargs):
    try:
        transaction = instance.transaction
        transaction.delete()
    except:
        pass


@receiver(post_save, sender=OrderItem)
def create_order_item(sender, instance, created, **kwargs):
    orderItem = instance
    if created == True:
        product = orderItem.product
        if product.qty < 0:
            product.qty -= orderItem.qty
            orderItem.price += product.price
    order = orderItem.order
    order.save()


@receiver(pre_save, sender=OrderItem)
def update_order_item(sender, instance, **kwargs):
    orderItem = instance
    product = instance.product
    orderItem.price = product.price * instance.qty
