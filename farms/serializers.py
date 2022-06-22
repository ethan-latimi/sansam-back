from dataclasses import field
from rest_framework import serializers
from .models import Farm, Log


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = '__all__'


class FarmImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Farm
        fields = ('image',)


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'


class LogImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Log
        fields = ('image',)
