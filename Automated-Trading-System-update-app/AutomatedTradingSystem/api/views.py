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
from django.http import JsonResponse
from django.shortcuts import redirect, render

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         # Get the username and password from the request
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('market')  # Redirect to the market page
#         else:
#             return JsonResponse({"message": "Invalid username or password"}, status=400)
#     else:
#         # If the request method is not POST, render the login form
#         return render(request, 'login.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Check if the content type is JSON
        if request.content_type == 'application/json':
            # Load JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        else:
            # If content type is not JSON, assume form data
            username = request.POST.get('username')
            password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('market')
        else:
            return JsonResponse({"message": "Invalid username or password"}, status=400)
    else:
        # If the request method is not POST, render the login form
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

def market(request):
    return render(request, 'market.html')

def wallet(request):
    return render(request, 'wallet.html')

def trading(request):
    return render(request, 'trading.html')

def watchlist(request):
    return render(request, 'watchlist.html')

def lichsu(request):
    return render(request, 'transaction_history.html')