from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
@permission_classes([])
def test_endpoint(request):
    logger.info(request.user) # If Authorization: Token ... is not provided, this will be AnonymousUser, otherwise it will be the user
    return HttpResponse("Hello from the backend!")

# wrap this function in an authentication decorator
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_endpoint_auth(request):
    logger.info(request.user) # Proves that auth token retrieves user data
    return HttpResponse("Hello from the backend! You are authenticated")


## Authentication views, these manage values that IsAuthenticated uses to determine if a user is authenticated

@api_view(['POST'])
@permission_classes([])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"token: {token}")
            return JsonResponse({'status': 'success', 'message': 'User Logged In', 'auth_token': token.key})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'}, status=400)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

@api_view(['POST'])
@permission_classes([])
def signup_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = User.objects.create_user(username=username, password=password)
        user.save()

        token = Token.objects.create(user=user)
        logger.info(f"token: {token}")
        return JsonResponse({'status': 'success', 'message': 'User Created', 'auth_token': token.key})
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logger.info(request.user)
    Token.objects.filter(user=request.user).delete()
    logout(request)
    return HttpResponse('Logout successful')
