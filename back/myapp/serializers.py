from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'ipaddress']
        extra_kwargs = {
            'password': {'write_only': True},
            'ipaddress': {'required': False}
        }
