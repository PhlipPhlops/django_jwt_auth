from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import logging

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['GET'])
@permission_classes([])
def test_endpoint(request):
    logger.info(request.user)
    return HttpResponse("Hello from the backend!")

# wrap this function in an authentication decorator
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_endpoint_auth(request):
    logger.info(request.user)
    return HttpResponse("Hello from the backend! You are authenticated")


@api_view(['POST'])
@permission_classes([])
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('Login successful')
    else:
        return HttpResponse('Invalid username or password')

@api_view(['POST'])
@permission_classes([])
def signup_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return HttpResponse('User created')

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return HttpResponse('Logout successful')
