from django.urls import path, include
from . import views

urlpatterns = [
    path("organizer", views.organizer_view, name='organizer'),
    path('', views.index, name='index'),
    path("organiser/event/<int:event_id>", views.organiser_event_view, name='organiser_event'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index/', views.HomeView.as_view(), name='Home'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
    path('events/', views.events, name='events'),
    

]
