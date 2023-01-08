from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response('Hello world!')

