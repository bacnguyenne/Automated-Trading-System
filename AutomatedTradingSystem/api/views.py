from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# View dựa trên lớp để Lấy chi tiết Người dùng bằng Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# View dựa trên lớp để đăng ký người dùng
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Logged in successfully',
                'username': username,
                'is_admin': user.is_superuser
            })
        else:
            return JsonResponse({"message": "Invalid username or password"}, status=400)
    else:
        # Render the login form
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        if password != confirm_password:
            return HttpResponse("Passwords do not match")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Error in user creation")
    else:
        return render(request, 'register.html')
    

from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')