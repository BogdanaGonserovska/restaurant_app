from django.urls import path
from . import views


urlpatterns = [
    path('register', views.create_user, name='register'),
    path('logout', views.logout, name='logout'),
    path('users', views.get_users, name='users'),
    path('user', views.user_view, name='user'),
    path('restaurant/<int:id>', views.restaurant_view_id, name='restaurant'),
    path('consumers', views.get_consumers, name='consumers'),
    path('restaurants', views.get_restaurants, name='restaurants'),
    path('menu', views.menu_view, name='menu'),
    path('menu/<int:id>', views.menu_view_id, name='menu_id'),
    path('dish', views.dish_view, name='dish'),
    path('dish/<int:id>', views.dish_view_id, name='dish_id'),
    path('order', views.order_view, name='order'),
    path('dish_for_order', views.order_dish, name='dish_order')
]