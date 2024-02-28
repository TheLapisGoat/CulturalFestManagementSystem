from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("organizer", views.organiser_view, name='organiser'),
]
