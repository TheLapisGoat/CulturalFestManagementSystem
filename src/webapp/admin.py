from django.contrib import admin
from .models import User_Entity, Student, Volunteer, External_Participant, Organizer
# Register your models here.

admin.site.register(User_Entity)
admin.site.register(Student)
admin.site.register(Volunteer)
admin.site.register(External_Participant)
admin.site.register(Organizer)