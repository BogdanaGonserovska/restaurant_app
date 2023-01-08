from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'username', 'is_restaurant', 'menu_id')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('meal', 'picture', 'price', 'description')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date', 'menu_id', 'user_id')