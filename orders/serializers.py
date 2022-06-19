from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    customerName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_customerName(self, obj):
        customer = obj.customer.name
        return customer


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
