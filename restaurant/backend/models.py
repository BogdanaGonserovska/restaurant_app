from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    is_restaurant = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__ (self):
        return f'{self.username}' if self.is_restaurant else f'{self.first_name} {self.last_name}'       


class Menu(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Dish(models.Model):
    meal = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pics')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=1000)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)


class DishForOrder(models.Model):
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class Order(models.Model):
    date = models.DateTimeField(default=datetime.now)
    dish_id = models.ForeignKey(DishForOrder, on_delete=models.CASCADE, default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    restaurant_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant', default=None)
    table_number = models.IntegerField(default=1)
    
