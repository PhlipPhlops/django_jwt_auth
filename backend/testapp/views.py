from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

def test_endpoint(request):
    return HttpResponse("Hello from the backend!")


class LoginView(APIView):
    def post(self, request):
        serializer = JSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user:
                # The user is authenticated, generate and return a JWT token
                token = serializer.generate_token(user)
                return Response({'token': token})
            else:
                # The provided username and password are incorrect
                return Response(
                    {'error': 'Invalid username or password'},
                    status=401,
                )
        else:
            # The request data is invalid
            return Response(
                {'error': 'Invalid request data'},
                status=400,
            )
