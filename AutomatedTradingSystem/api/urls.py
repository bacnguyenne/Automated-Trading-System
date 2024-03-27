from django.urls import path
from api.views import UserDetailAPI, RegisterUserAPIView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('market/', views.market, name='market'),
    path('wallet/', views.wallet, name='wallet'),
    path('trading/', views.trading, name='trading'),
]