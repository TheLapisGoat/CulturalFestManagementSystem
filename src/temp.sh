#!/bin/bash

#Delete webapp/migrations
rm -rf webapp/migrations

# Run migrations
python manage.py makemigrations webapp
python manage.py migrate

# Define predefined user fields
username="admin"
password="admin"
first_name="Admin"
last_name="Admin"
email="a@b.com"
address_line_1="1234 Main St"
state="CA"
country="US"
pin_code="12345"
telephoneNumber="123456789"
role="admin"

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role')" | python manage.py shell

echo "Superuser created successfully:"
echo "Username: $username"
echo "Password: $password"

# Define organizer fields
organizer_username="organizer"
organizer_password="organizer"
organizer_first_name="Organizer"
organizer_last_name="Organizer"
organizer_email="organizer@example.com"
organizer_address_line_1="5678 Main St"
organizer_state="CA"
organizer_country="US"
organizer_pin_code="54321"
organizer_telephoneNumber="987654321"
organizer_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer_username', '$organizer_email', '$organizer_password', first_name='$organizer_first_name', last_name='$organizer_last_name', address_line_1='$organizer_address_line_1', state='$organizer_state', country='$organizer_country', pin_code='$organizer_pin_code', telephoneNumber='$organizer_telephoneNumber', role='$organizer_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer created successfully:"
echo "Username: $organizer_username"
echo "Password: $organizer_password"

# Define event fields
event_name1="Event 1"
event_description1="Description of Event 1"
event_name2="Event 2"
event_description2="Description of Event 2"
start_date="2024-03-01 10:00:00"
end_date="2024-03-02 10:00:00"
registration_start_date="2024-02-01 10:00:00"
registration_end_date="2024-02-28 10:00:00"
max_participants=50
min_participants=10

# Create events
echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer = Organizer.objects.get(user__username='$organizer_username'); venue = Venue.objects.create(venue_name='Your Venue', venue_capacity=100, address_line_1='Address Line 1'); event1 = Event.objects.create(name='$event_name1', description='$event_description1', start_date='$start_date', end_date='$end_date', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event1.organizers.add(organizer)" | python manage.py shell

echo "Event 1 created successfully."

echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer = Organizer.objects.get(user__username='$organizer_username'); venue = Venue.objects.create(venue_name='Your Venue', venue_capacity=100, address_line_1='Address Line 1'); event2 = Event.objects.create(name='$event_name2', description='$event_description2', start_date='$start_date', end_date='$end_date', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event2.organizers.add(organizer)" | python manage.py shell

echo "Event 2 created successfully."

# Run the server
python manage.py runserver
