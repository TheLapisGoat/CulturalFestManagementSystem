from django.urls import path, include
from . import views

urlpatterns = [
    path("organizer", views.organizer_view, name='organizer'),
    path('', views.index, name='index'),
    path("organizer/event/<int:event_id>", views.organizer_event_view, name='organizer_event'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index/', views.HomeView.as_view(), name='Home'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
    path('events/', views.events, name='events'),
    path('participant',views.participant_view.as_view(), name='participant'),
    path('participant/register/<int:event_id>',views.participant_register_view.as_view(),name="participant_register"),
    path('participant/event/<int:event_id>',views.participant_event_view.as_view(),name="participant_event"),
    path('participant/profile',views.participant_profile_view.as_view(),name="participant_profile"),

]
