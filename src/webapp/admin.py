from django.contrib import admin
from .models import User_Entity, Student, Volunteer, External_Participant, Organizer, Event, Venue, Organized_by, Organizer_Key
# Register your models here.

admin.site.register(User_Entity)
admin.site.register(Student)
admin.site.register(Volunteer)
admin.site.register(External_Participant)
admin.site.register(Organizer)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Organized_by)
admin.site.register(Organizer_Key)