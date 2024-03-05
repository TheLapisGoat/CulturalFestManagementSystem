from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import External_Participant, Accomodation, Participant_Accomodation
import random

@receiver(post_save, sender=External_Participant)
def allocate_accommodation(sender, instance, created, **kwargs):
    if created:
        accomodations = Accomodation.objects.all()
        accomodation = random.choice(accomodations)
        participant_accomodation = Participant_Accomodation.objects.create(participant=instance, accomodation=accomodation)
        participant_accomodation.room_number = accomodation.next_free_room
        accomodation.next_free_room += 1
        participant_accomodation.save()
        accomodation.save()