from django.urls import path
from api.views import UserDetailAPI, RegisterUserAPIView
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path("get-details/", UserDetailAPI.as_view()),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('market/', views.market, name='market')
=======
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('market/', views.market, name='market'),
    path('wallet/', views.wallet, name='wallet'),
    path('trading/', views.trading, name='trading'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('lichsu/', views.lichsu, name='lichsu'),
>>>>>>> Stashed changes
]