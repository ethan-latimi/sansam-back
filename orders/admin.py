from django.contrib import admin

from . import models

admin.site.register(models.OrderImage)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """ Customized Order Admin """
    list_display = (
        "customer",
        "price",
        "items",
        "payment",
        "isPaid",
        "isDelivered",
        "images",
        "receiver",
    )

    def items(self, obj):
        return obj.orderItems.count()

    def images(self, obj):
        return obj.orderImages.count()


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    """ Customized OrderItem Admin """

    list_display = (
        'product',
        'qty',
        'price',
        'order',
    )
