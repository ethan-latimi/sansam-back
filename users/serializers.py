# Rest Framework
from rest_framework import serializers

# Project
from .models import User


class UserSerializer(serializers.ModelSerializer):

    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'gender', 'isAdmin', 'bio', ]

    def get_isAdmin(self, obj):
        return obj.is_staff
