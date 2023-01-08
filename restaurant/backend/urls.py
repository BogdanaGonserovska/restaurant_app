from django.urls import path
from . import views


urlpatterns = [
    path('hello', views.hello_world, name='hello'),
    path('register', views.create_user, name='register'),
    path('logout', views.logout, name='logout'),
    path('users', views.get_users, name='users'),
    path('user', views.user_view, name='user'),
    path('consumers', views.get_consumers, name='consumers'),
    path('restaurants', views.get_restaurants, name='restaurants'),
]