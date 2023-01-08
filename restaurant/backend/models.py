from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


class Menu(models.Model):
    meal = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pics')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=1000)


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)
    is_restaurant = models.BooleanField(default=False)
    menu_id = models.OneToOneField(Menu, on_delete=models.CASCADE, null=True)

    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__ (self):
        if self.is_restaurant == False:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'


class Order(models.Model):
    date = models.DateTimeField(default=datetime.now)
    menu_id = models.ManyToManyField(Menu)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
