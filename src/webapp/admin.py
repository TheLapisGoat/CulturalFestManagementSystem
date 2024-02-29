from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User_Entity)
admin.site.register(Student)
admin.site.register(Volunteer)
admin.site.register(External_Participant)
admin.site.register(Organizer)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Organized_by)
admin.site.register(Volunteer_event)
admin.site.register(Organizer_Key)
admin.site.register(Venue_schedule_event)
admin.site.register(Infra_schedule)