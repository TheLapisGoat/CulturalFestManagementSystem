from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path("organizer/", views.organizer_view, name='organizer'),
    path("organizer/profile/", views.organizer_profile_view, name='organizer_profile'),
    path("organizer/event/<int:event_id>", views.organizer_event_view, name='organizer_event'),

    path("student/", views.student_view, name='student'),
    path("student/profile/", views.student_profile_view, name='student_profile'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),

    path('index/', views.HomeView.as_view(), name='Home'),


    path('events/', views.events, name='events'),
]
