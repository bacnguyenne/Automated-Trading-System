from django.urls import path
from api.views import UserDetailAPI, RegisterUserAPIView
from . import views

urlpatterns = [
    path("get-details/", UserDetailAPI.as_view()),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
]