from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .forms import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django.forms.models import model_to_dict
from datetime import datetime


@api_view(['POST'])
def create_user(request):
    form = UserForm(request.data)
    if form.is_valid():
        user = form.save()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'user logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'message': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    users_serialized = UserSerializer(users, many=True)
    return Response(users_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def user_view(request):
    if request.method == 'GET':
        try:
            user = request.user
            user_serialized = UserSerializer(user)
            if user_serialized.data['is_restaurant']:
                user_data = user_serialized.data
                menu = Menu.objects.filter(user_id=user)
                menu_serializer = MenuSerializer(menu, many=True)
                menu_data = menu_serializer.data
                for m in menu_data:
                    dishes = Dish.objects.filter(menu_id=m['id'])
                    dish_serializer = DishSerializer(dishes, many=True)
                    m['dishes'] = dish_serializer.data
                user_data['menus'] = menu_serializer.data
                return Response(user_data, status=status.HTTP_200_OK)
            return Response(user_serialized.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        try:
            user = request.user
            user.delete()
            return Response({'message': 'user successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def restaurant_view_id(request, id):
    if request.method == 'GET':    
        try:
            user = User.objects.get(id=id)
            user_serialized = UserSerializer(user)
            if user_serialized.data['is_restaurant']:
                user_data = user_serialized.data
                menu = Menu.objects.filter(user_id=id)
                menu_serializer = MenuSerializer(menu, many=True)
                menu_data = menu_serializer.data
                for m in menu_data:
                    dishes = Dish.objects.filter(menu_id=m['id'])
                    dish_serializer = DishSerializer(dishes, many=True)
                    m['dishes'] = dish_serializer.data
                user_data['menus'] = menu_serializer.data
                return Response(user_data, status=status.HTTP_200_OK)
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_consumers(request):
    consumers = User.objects.filter(is_restaurant=False)
    consumers_serialized = UserSerializer(consumers, many=True)
    return Response(consumers_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_restaurants(request):
    restaurants = User.objects.filter(is_restaurant=True)
    restaurants_serialized = UserSerializer(restaurants, many=True)
    return Response(restaurants_serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def menu_view(request):
    if request.method == 'POST':
        name = request.data['name']
        user_id = request.user

        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if user_id.is_restaurant:
            menu = Menu(name=name, user_id=user_id)
            serializer = MenuSerializer(data=model_to_dict(menu))
            if not serializer.is_valid():
                return Response({'message': 'invalid values'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                menu.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)  
        return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT', 'DELETE'])
def menu_view_id(request, id):

    if request.method == 'PUT':
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_restaurant == False:
            return Response({'message': 'not restaurant'}, status=status.HTTP_403_FORBIDDEN)
        try:
            menu = Menu.objects.get(id=id)
        except:
            return Response({'message': 'menu not found'}, status=status.HTTP_404_NOT_FOUND)
        menu_data=request.data
        menu_data['user_id'] = user.id
        serializer = MenuSerializer(instance=menu, data=menu_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_restaurant == False:
            return Response({'message': 'not restaurant'}, status=status.HTTP_403_FORBIDDEN)
        try:
            menu = Menu.objects.get(id=id)
            menu.delete()
            return Response({'message': 'menu deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'menu not found'}, status=status.HTTP_404_NOT_FOUND)
       

@api_view(['POST'])
def dish_view(request):
    if request.method == 'POST':
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_restaurant:
            dish = DishSerializer(data=request.data)
            if not dish.is_valid():
                return Response({'message': 'invalid values'}, status=status.HTTP_400_BAD_REQUEST)           
            try:
                dish.save()
                return Response(dish.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT', 'DELETE'])
def dish_view_id(request, id):
    if request.method == 'PUT':
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            dish = Dish.objects.get(id=id)
        except:
            return Response({'message': 'dish not found'}, status=status.HTTP_404_NOT_FOUND)
       
        menu = Menu.objects.get(id=dish.menu_id.id)
        if menu.user_id != user:
            return Response({'message': 'not your restaurant'}, status=status.HTTP_403_FORBIDDEN)
        dish_data = request.data
        dish_data['menu_id'] = dish.menu_id.id
        serializer = DishSerializer(instance=dish, data=dish_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            dish = Dish.objects.get(id=id)
            menu = Menu.objects.get(id=dish.menu_id.id)
            if menu.user_id != user:
                return Response({'message': 'not your restaurant'}, status=status.HTTP_403_FORBIDDEN)
            dish.delete()
            return Response({'message': 'dish deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'dish not found'}, status=status.HTTP_404_NOT_FOUND)


