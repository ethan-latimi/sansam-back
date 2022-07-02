from rest_framework import serializers

from orders.models import Order
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("id", "sellerMemo", "customerMemo", "created")
