from django.urls import path, include
from . import views

urlpatterns = [
    path("organizer", views.organizer_view, name='organizer'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index/', views.HomeView.as_view(), name='Home'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
]
