from rest_framework import serializers
from orders.models import Order, OrderImage, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    customerName = serializers.SerializerMethodField(read_only=True)
    phoneNumber = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_customerName(self, obj):
        customer = obj.customer.name
        return customer

    def get_phoneNumber(self, obj):
        phoneNumber = obj.customer.phoneNumber
        return phoneNumber


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product(self, obj):
        product = obj.product.name
        return product


class OrderImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderImage
        fields = '__all__'
