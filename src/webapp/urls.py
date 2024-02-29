from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("organizer", views.organiser_view, name='organiser'),
    path("organiser/event/<int:event_id>", views.organiser_event_view, name='organiser_event'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
