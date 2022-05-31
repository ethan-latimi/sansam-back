from rest_framework import serializers
from .models import Farm, Log


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'
