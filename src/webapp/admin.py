from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .forms import *

class User_Entity_Admin(UserAdmin):
    add_form = User_EntityCreationForm
    form = User_EntityChangeForm
    model = User_Entity
    list_display = ('username', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'state', 'country', 'pin_code', 'telephoneNumber', 'photograph', 'gender', 'date_of_birth', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'middle_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'state', 'country', 'pin_code', 'telephoneNumber', 'photograph', 'gender', 'date_of_birth', 'is_active', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class Student_Admin(ModelAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student
    list_display = ('user', 'roll_number', 'department')
    list_filter = ('department',)
    fieldsets = (
        (None, {'fields': ('user', 'roll_number', 'department')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'roll_number', 'department'),
        }),
    )
    search_fields = ('user', 'roll_number', 'department')
    ordering = ('user',)

class Volunteer_Admin(ModelAdmin):
    add_form = VolunteerCreationForm
    form = VolunteerChangeForm
    model = Volunteer
    
    def username(self, obj):
        return obj.student.user.username

    list_display = ('username', 'hours')
    fieldsets = (
        (None, {'fields': ('student', 'hours')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student', 'hours'),
        }),
    )
    search_fields = ('student', 'hours')
    ordering = ('student',)

class External_Participant_Admin(ModelAdmin):
    add_form = External_ParticipantCreationForm
    form = External_ParticipantChangeForm
    model = External_Participant
    list_display = ('user', 'organization',)
    list_filter = ('organization',)
    fieldsets = (
        (None, {'fields': ('user', 'organization',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'organization',),
        }),
    )
    search_fields = ('user', 'organization',)
    ordering = ('user',)

class Organizer_Admin(ModelAdmin):
    add_form = OrganizerCreationForm
    form = OrganizerChangeForm
    model = Organizer
    list_display = ('user',)
    fieldsets = (
        (None, {'fields': ('user',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user',),
        }),
    )
    search_fields = ('user',)
    ordering = ('user',)


admin.site.register(User_Entity, User_Entity_Admin)
admin.site.register(Student, Student_Admin)
admin.site.register(Volunteer, Volunteer_Admin)
admin.site.register(External_Participant, External_Participant_Admin)
admin.site.register(Organizer, Organizer_Admin)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Organizer_Key)
admin.site.register(Venue_schedule_event)
admin.site.register(Infra_schedule)
admin.site.register(EventResults)
admin.site.register(Participant_Accomodation)
admin.site.register(Accomodation)
admin.site.site_header = 'Festival Management System Administration'