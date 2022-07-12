from rest_framework import serializers
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['wallet']


class TransactionSerializer(serializers.ModelSerializer):
    customerName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_customerName(self, obj):
        customer = obj.customer.name
        return customer
