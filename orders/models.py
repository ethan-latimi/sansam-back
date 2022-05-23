from django.db import models
from django.dispatch import receiver

from core.models import TimeStampedModel
from customers.models import Customer
from products.models import Product


class Order(TimeStampedModel):

    """ Order Model (주문)"""
    PAYMENT_CASH = 'cash'
    PAYMENT_CARD = 'card'
    PAYMENT_METHODS = (
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_CARD, 'Card')
    )

    id = models.AutoField(primary_key=True, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    payment = models.CharField(choices=PAYMENT_METHODS, max_length=100)
    price = models.IntegerField(default=0)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deleveredAt = models.DateTimeField(null=True, blank=True)
    receiver = models.CharField(
        max_length=100, null=True, default=customer, blank=True)
    customerMemo = models.CharField(max_length=255, null=True, blank=True)
    sellerMemo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.customer} order {self.id}"


class OrderItem(models.Model):

    """ Order Item Model (각 주문 항목)"""

    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField(default=0)
    price = models.IntegerField()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderItems')

    def __str__(self):
        return self.product.name


class OrderImage(models.Model):

    """ Order's Image Model (최종 확인용 사진)"""

    name = models.CharField(max_length=255)
    image = models.ImageField()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderImages')

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):

    """ Shipping Address (배달지)"""

    address = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=1024)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='orderAddress')

    def __str__(self):
        return f"Address: {self.order}"
