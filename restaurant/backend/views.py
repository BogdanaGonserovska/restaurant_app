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
def get_consumers(request):
    consumers = User.objects.filter(is_restaurant=False)
    consumers_serialized = UserSerializer(consumers, many=True)
    return Response(consumers_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_restaurants(request):
    restaurants = User.objects.filter(is_restaurant=True)
    restaurants_serialized = UserSerializer(restaurants, many=True)
    return Response(restaurants_serialized.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def menu_view(request):
    if request.method == 'POST':
        meal = request.data['meal']
        picture = request.data['picture']
        price = request.data['price']
        description = request.data['description']
        user_id = request.user

        if user_id.is_restaurant == True:
            menu = Menu(meal=meal, picture=picture, price=price, description=description, user_id=user_id)
            serializer = MenuSerializer(data=model_to_dict(menu))
            if not serializer.is_valid():
                return Response({'message': 'invalid values'}, status=status.HTTP_400_BAD_REQUEST)
            if isinstance(request.user, AnonymousUser):
                return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                menu.save()
            except IntegrityError as e:
                return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            user = request.user
            if isinstance(request.user, AnonymousUser):
                return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_restaurant == False:
                return Response({'message': 'not restaurant'}, status=status.HTTP_403_FORBIDDEN)
            menu = Menu.objects.filter(user_id=user)
            serializer = MenuSerializer(menu, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
def get_menu(request, id):
    if request.method == 'GET':
        try:
            if User.objects.get(id=id).is_restaurant == False:
                return Response({'message': 'not restaurant'}, status=status.HTTP_404_NOT_FOUND)
            menu = Menu.objects.filter(user_id = id)
            serializer = MenuSerializer(menu, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_restaurant == False:
            return Response({'message': 'not restaurant'}, status=status.HTTP_403_FORBIDDEN)

        menu = Menu.objects.get(id=id)
        serializer = MenuSerializer(instance=menu, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)