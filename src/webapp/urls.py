from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.MainViewRedirect.as_view(), name='index-redirector'),
    path("admin/", admin.site.urls),
    path("admin/", admin.site.index, name = "admin-home"),

    path("organizer/event/<int:event_id>", views.OrganizerEventView.as_view(), name='organizer-event'),
    path('organizer/profile/', views.OrganizerProfileView.as_view(), name='organizer-profile'),
    path('organizer/logistics/', views.OrganizerLogisticsView.as_view(), name='organizer-volunteer'),
    path("organizer/", views.OrganizerHomeView.as_view(), name='organizer-home'),
    path("organizer/register_event/", views.Register_Event_View.as_view(), name='organizer-event-register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),

    path('index/', views.HomeView.as_view(), name='Home'),

    path('student/', views.student_home_view.as_view(), name='student-home'),
    path('student/volunteer_redirect/', views.student_volunteer_redirect.as_view(), name='student-volunteer-view-redirector'),
    path('student/register_volunteer/', views.student_register_volunteer_view.as_view(), name='student-register-volunteer'),
    path('student/volunteer/', views.student_volunteer_view.as_view(), name='student-volunteer'),
    path('student/profile/', views.student_profile_view.as_view(), name='student-profile'),



    path('events/', views.events, name='events'),
    path('participant',views.participant_view.as_view(), name='external-participant-home'),
    path('participant/register/<int:event_id>',views.participant_register_view.as_view(),name="participant_register"),
    path('participant/event/<int:event_id>',views.participant_event_view.as_view(),name="participant_event"),
    path('participant/profile',views.participant_profile_view.as_view(),name="participant_profile"),
    path('participant/accomodation',views.participant_view_accomodation.as_view(),name="participant_accomodation"),

    path('logout/', views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
