from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
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


## Authentication views, these manage values that IsAuthenticated uses to determine if a user is authenticated

@api_view(['POST'])
@permission_classes([])
def login_user(request):
    logger.info(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    logger.info(f'username: {username}, password: {password}') # Query dict is failing, clearly an environment issue
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        # Use the ObtainAuthToken view to generate an authentication token
        response = obtain_auth_token(request._request)

        # Return the authentication token in the response
        return Response({'auth_token': response.data['token']})
    else:
        return HttpResponse('Invalid username or password')

@api_view(['POST'])
@permission_classes([])
def signup_user(request):
    logger.info(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    logger.info(f'username: {username}, password: {password}')
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return HttpResponse('User created')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return HttpResponse('Logout successful')
