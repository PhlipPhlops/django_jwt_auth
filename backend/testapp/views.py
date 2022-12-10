from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
import logging

logger = logging.getLogger(__name__)

# Auth notes
# SessionAuthentication is used to authenticate a user using a session cookie, eg
# curl -X POST -b "sessionid=abc123" http://localhost:8000/my_view/
# BasicAuthentication is used to authenticate a user using HTTP Basic Auth, eg
# curl -X POST -u "username:password" http://localhost:8000/my_view/
# TokenAuthentication is used to authenticate a user using a JWT token, eg
# curl -X POST -H "Authorization Token abc123" http://localhost:8000/my_view/


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
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        # Do something with the data...
        logger.info(f'username: {username}, password: {password}')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = obtain_auth_token(request._request)
            logger.info("response: %s", response.data)
            return JsonResponse({'status': 'success', 'message': 'User Logged In', 'auth_token': response.data['token']})
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
        # Do something with the data...
        logger.info(f'username: {username}, password: {password}')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User Created'})
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logger.info(request.user)
    logout(request)
    return HttpResponse('Logout successful')
