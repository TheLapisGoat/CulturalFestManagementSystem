from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.MainViewRedirect.as_view(), name='index-redirector'),
    path("admin/", admin.site.urls),
    path("admin/", admin.site.index, name = "admin-home"),

    path("organizer/event/<int:event_id>", views.OrganizerEventView.as_view(), name='organizer-event'),
    path('organizer/profile/', views.OrganizerProfileView.as_view(), name='organizer-profile'),
    path("organizer/", views.OrganizerHomeView.as_view(), name='organizer-home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),

    path('index/', views.HomeView.as_view(), name='Home'),

    path('student/', views.StudentHomeView.as_view(), name='student-home'),
    path('student/volunteer/', views.StudentVolunteerView.as_view(), name='student-volunteer'),
    path('student/register_volunteer/', views.StudentRegisterVolunteerView.as_view(), name='student-register-volunteer'),
    path('student/profile/', views.StudentProfileView.as_view(), name='student-profile'),



    path('events/', views.events, name='events'),
    path('participant',views.participant_view.as_view(), name='external-participant-home'),
    path('participant/register/<int:event_id>',views.participant_register_view.as_view(),name="participant_register"),
    path('participant/event/<int:event_id>',views.participant_event_view.as_view(),name="participant_event"),
    path('participant/profile',views.participant_profile_view.as_view(),name="participant_profile"),

    path('logout/', views.LogoutView.as_view(), name='logout'),
]
