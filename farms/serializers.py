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
    farmName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Log
        fields = '__all__'

    def get_farmName(self, obj):
        farmName = obj.farm.title
        return farmName


class LogImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Log
        fields = ('image',)
