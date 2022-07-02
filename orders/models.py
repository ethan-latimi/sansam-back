from django.db import models

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
    PAID_FINISH = True
    PAID_YET = False
    PAID_REFUND = "refund"
    PAID_CHOICES = (
        (PAID_FINISH, 'Cash'),
        (PAID_YET, 'Card'),
        (PAID_REFUND, 'Refund')
    )

    id = models.AutoField(primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    payment = models.CharField(
        choices=PAYMENT_METHODS, max_length=100, null=True)
    price = models.IntegerField(default=0)
    isPaid = models.CharField(choices=PAID_CHOICES,
                              default=PAID_FINISH, max_length=100)
    paidAt = models.DateTimeField(null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(null=True, blank=True)
    receiver = models.CharField(
        max_length=100, null=True, default="", blank=True)
    customerMemo = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    sellerMemo = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.customer} order {self.id}"


class OrderItem(models.Model):

    """ Order Item Model (각 주문 항목)"""

    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.SET_DEFAULT, default="존재하지 않음", related_name="orderItem")
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderItems')

    def __str__(self):
        return self.product.id


class OrderImage(models.Model):

    """ Order's Image Model (최종 확인용 사진)"""

    id = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderImages')

    def __str__(self):
        return self.id


class ShippingAddress(models.Model):

    """ Shipping Address (배달지)"""

    address = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=1024)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='orderAddress')

    def __str__(self):
        return f"Address: {self.order}"
