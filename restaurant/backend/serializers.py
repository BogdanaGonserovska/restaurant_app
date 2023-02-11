from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'username', 'is_restaurant')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'user_id')


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'meal', 'picture', 'price', 'description', 'menu_id')


class DishForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishForOrder
        fields = ('id', 'dish_id', 'count', 'order_id')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date', 'user_id', 'restaurant_id', 'table_number')