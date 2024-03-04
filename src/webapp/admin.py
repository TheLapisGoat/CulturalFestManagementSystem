from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .forms import *
from django.contrib import messages

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

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.add_form
        # Get the form
        form = super().get_form(request, obj, **kwargs)
        # Filter the queryset for the user field to exclude users associated with any student
        form.base_fields['user'].queryset = User_Entity.objects.filter(student__isnull=True)
        return form

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

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.add_form
        # Get the form
        form = super().get_form(request, obj, **kwargs)
        # Filter the queryset for the student field to exclude students associated with any volunteer
        form.base_fields['student'].queryset = Student.objects.filter(volunteer__isnull=True)
        return form

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

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.add_form
        # Get the form
        form = super().get_form(request, obj, **kwargs)
        # Filter the queryset for the user field to exclude users associated with any external participant
        form.base_fields['user'].queryset = User_Entity.objects.filter(external_participant__isnull=True)
        return form

class Organizer_Admin(ModelAdmin):
    add_form = OrganizerCreationForm
    form = OrganizerChangeForm
    model = Organizer
    list_display = ('user', 'name')
    fieldsets = (
        (None, {'fields': ('user',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user',),
        }),
    )
    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    search_fields = ('user',)
    ordering = ('user',)

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.add_form
        # Get the form
        form = super().get_form(request, obj, **kwargs)
        # Filter the queryset for the user field to exclude users associated with any organizer
        form.base_fields['user'].queryset = User_Entity.objects.filter(organizer__isnull=True)
        return form
    
class Venue_Admin(ModelAdmin):
    list_display = ('name', 'capacity')
    fieldsets = (
        (None, {'fields': ('name', 'address_line_1', 'address_line_2', 'capacity')}),
    )
    search_fields = ('name', 'address_line_1', 'address_line_2', 'capacity')
    ordering = ('name',)

class Event_Admin(ModelAdmin):
    list_display = ('name', 'venue', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'venue', 'start_date', 'end_date')
    ordering = ('name',)

    def save_related(self, request, form, formsets, change):
        # Check for any venue bookings that clash with the new event's start and end dates
        venue = form.instance.venue
        if venue is not None:
            for event in Event.objects.filter(venue=venue):
                if (event.start_date <= form.instance.start_date <= event.end_date) or (event.start_date <= form.instance.end_date <= event.end_date):
                    self.message_user(request, "The event clashes with another event at the same venue", level=messages.ERROR)
                    # Delete the event
                    form.instance.delete()
                    return
        # Check that min_participants <= max_participants
        if form.instance.min_participants > form.instance.max_participants:
            self.message_user(request, "The minimum number of participants cannot be greater than the maximum number of participants", level=messages.ERROR)
            # Delete the event
            form.instance.delete()
            return
        super().save_related(request, form, formsets, change)

class Accomodation_Admin(ModelAdmin):
    list_display = ('accomodation_name', 'cost_per_night')
    search_fields = ('accomodation_name', 'address_line_1', 'address_line_2')
    ordering = ('accomodation_name',)



admin.site.register(User_Entity, User_Entity_Admin)
admin.site.register(Student, Student_Admin)
admin.site.register(Volunteer, Volunteer_Admin)
admin.site.register(External_Participant, External_Participant_Admin)
admin.site.register(Organizer, Organizer_Admin)
admin.site.register(Venue, Venue_Admin)
admin.site.register(Event, Event_Admin)
admin.site.register(Organizer_Key)
admin.site.register(EventResults)
admin.site.register(Participant_Accomodation)
admin.site.register(Accomodation, Accomodation_Admin)
admin.site.site_header = 'Festival Management System Administration'