from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import UserProfileUpdateView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
]
