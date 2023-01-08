from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .forms import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response('Hello world!')

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
