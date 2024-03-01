from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.MainViewRedirect.as_view(), name='index-redirector'),
    path("admin/", admin.site.urls),
    path("admin/", admin.site.index, name = "admin-home"),
    path("organizer/event/<int:event_id>", views.organiser_event_view, name='organizer-event'),
    path("organizer", views.OrganizerHomeView.as_view(), name='organizer-home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index/', views.HomeView.as_view(), name='Home'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
]
