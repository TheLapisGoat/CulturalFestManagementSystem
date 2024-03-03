#!/bin/bash

# delete old db
psql -U postgres -d template1 << EOF
DROP DATABASE IF EXISTS postgres;
CREATE DATABASE postgres;
\q
EOF
#Delete webapp/migrations
rm -rf webapp/migrations

# Run migrations
python3 manage.py makemigrations webapp
python3 manage.py migrate

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

# create organizer 2
organizer2_username="organizer2"
organizer2_password="organizer2"
organizer2_first_name="Organizer2"
organizer2_last_name="Organizer2"
organizer2_email="org2@org2.com"
organizer2_address_line_1="5678 Main St"
organizer2_state="CA"
organizer2_country="US"
organizer2_pin_code="54321"
organizer2_telephoneNumber="987654321"
organizer2_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer2_username', '$organizer2_email', '$organizer2_password', first_name='$organizer2_first_name', last_name='$organizer2_last_name', address_line_1='$organizer2_address_line_1', state='$organizer2_state', country='$organizer2_country', pin_code='$organizer2_pin_code', telephoneNumber='$organizer2_telephoneNumber', role='$organizer2_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer 2 created successfully:"
echo "Username: $organizer2_username"
echo "Password: $organizer2_password"

# create Organizer 3
organizer3_username="organizer3"
organizer3_password="organizer3"
organizer3_first_name="Organizer3"
organizer3_last_name="Organizer3"
organizer3_email="org3@org3.com"
organizer3_address_line_1="5678 Main St"
organizer3_state="CA"
organizer3_country="US"
organizer3_pin_code="54321"
organizer3_telephoneNumber="987654321"
organizer3_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer3_username', '$organizer3_email', '$organizer3_password', first_name='$organizer3_first_name', last_name='$organizer3_last_name', address_line_1='$organizer3_address_line_1', state='$organizer3_state', country='$organizer3_country', pin_code='$organizer3_pin_code', telephoneNumber='$organizer3_telephoneNumber', role='$organizer3_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer 3 created successfully:"
echo "Username: $organizer3_username"
echo "Password: $organizer3_password"

# Define event fields
event_name1="Event 1"
event_description1="Description of Event 1"
event_name2="Event 2"
event_description2="Description of Event 2"
start_date1="2024-03-01 10:00:00"
end_date1="2024-03-02 10:00:00"
start_date2="2024-03-03 10:00:00"
end_date2="2024-03-04 10:00:00"
registration_start_date="2024-02-01 10:00:00"
registration_end_date="2024-02-28 10:00:00"
max_participants=50
min_participants=10

# Create events
echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer = Organizer.objects.get(user__username='$organizer_username'); venue = Venue.objects.create(name='Venue 1', capacity=100, address_line_1='Address Line 1'); event1 = Event.objects.create(name='$event_name1', description='$event_description1', start_date='$start_date1', end_date='$end_date1', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event1.organizers.add(organizer)" | python manage.py shell

echo "Event 1 created successfully."

echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer = Organizer.objects.get(user__username='$organizer_username'); venue = Venue.objects.create(name='Venue 2', capacity=100, address_line_1='Address Line 1'); event2 = Event.objects.create(name='$event_name2', description='$event_description2', start_date='$start_date2', end_date='$end_date2', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event2.organizers.add(organizer)" | python manage.py shell

echo "Event 2 created successfully."

# Create Ext Participant
username="exp"
password="exp"
organization="exp"
email="exp@exp.exp"
address_line_1="exp"
address_line_2="exp"
state="exp"
first_name="exp"
last_name="exp"
country="exp"
pin_code="00000"
telephoneNumber="0000000000"
role="external_participant"

echo "from django.contrib.auth import get_user_model; from webapp.models import External_Participant; User = get_user_model(); user = User.objects.create_user('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', address_line_2='$address_line_2', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role'); External_Participant.objects.create(user=user, organization='$organization')" | python manage.py shell
echo "CREATED EXTERNAL PARTICIPANT SUCCESSFULLY"

# Create a Student
username="student"
password="student"
email="stud@stud.com"
address_line_1="1234 Main St"
state="CA"
country="US"
pin_code="12345"
telephoneNumber="123456789"
role="student"
first_name="Student"
last_name="Student"
roll_number="123456789"
department="CSE"

echo "from django.contrib.auth import get_user_model; from webapp.models import Student; User = get_user_model(); user = User.objects.create_user('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role'); Student.objects.create(user=user, roll_number='$roll_number', department='$department')" | python manage.py shell
echo "CREATED STUDENT SUCCESSFULLY"

# Run the server
python3 manage.py runserver
