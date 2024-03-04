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
first_name="Admin_First"
last_name="Admin_Last"
email="admin@admin.com"
address_line_1="1234 Main St"
state="CA"
country="US"
pin_code="12345"
telephoneNumber="1234567890"
role="admin"

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role')" | python manage.py shell

echo "Superuser created successfully:"
echo "Username: $username"
echo "Password: $password"

# Define organizer fields
organizer_username="organizer"
organizer_password="organizer"
organizer_first_name="Alan"
organizer_last_name="Turing"
organizer_email="organizer@organizer.com"
organizer_address_line_1="5678 Main St"
organizer_state="CA"
organizer_country="US"
organizer_pin_code="54321"
organizer_telephoneNumber="9876543210"
organizer_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer_username', '$organizer_email', '$organizer_password', first_name='$organizer_first_name', last_name='$organizer_last_name', address_line_1='$organizer_address_line_1', state='$organizer_state', country='$organizer_country', pin_code='$organizer_pin_code', telephoneNumber='$organizer_telephoneNumber', role='$organizer_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer created successfully:"
echo "Username: $organizer_username"
echo "Password: $organizer_password"

# create organizer 2
organizer2_username="organizer2"
organizer2_password="organizer2"
organizer2_first_name="Bjarne"
organizer2_last_name="Stroustrup"
organizer2_email="organizer2@organizer2.com"
organizer2_address_line_1="567 Main St"
organizer2_state="CA"
organizer2_country="US"
organizer2_pin_code="54321"
organizer2_telephoneNumber="9876543210"
organizer2_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer2_username', '$organizer2_email', '$organizer2_password', first_name='$organizer2_first_name', last_name='$organizer2_last_name', address_line_1='$organizer2_address_line_1', state='$organizer2_state', country='$organizer2_country', pin_code='$organizer2_pin_code', telephoneNumber='$organizer2_telephoneNumber', role='$organizer2_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer 2 created successfully:"
echo "Username: $organizer2_username"
echo "Password: $organizer2_password"

# create Organizer 3
organizer3_username="organizer3"
organizer3_password="organizer3"
organizer3_first_name="Larry"
organizer3_last_name="Page"
organizer3_email="organizer3@organizer3.com"
organizer3_address_line_1="678 Main St"
organizer3_state="CA"
organizer3_country="US"
organizer3_pin_code="54321"
organizer3_telephoneNumber="9876543210"
organizer3_role="organizer"

# Create organizer
echo "from django.contrib.auth import get_user_model; from webapp.models import Organizer; User = get_user_model(); user = User.objects.create_user('$organizer3_username', '$organizer3_email', '$organizer3_password', first_name='$organizer3_first_name', last_name='$organizer3_last_name', address_line_1='$organizer3_address_line_1', state='$organizer3_state', country='$organizer3_country', pin_code='$organizer3_pin_code', telephoneNumber='$organizer3_telephoneNumber', role='$organizer3_role'); Organizer.objects.create(user=user)" | python manage.py shell

echo "Organizer 3 created successfully:"
echo "Username: $organizer3_username"
echo "Password: $organizer3_password"

# Create Venue 1
venue_name1="Takshashila"
venue_capacity1="100"
venue_address_line_1="8886+RMQ, IIT Kharagpur"
venue_address_line_2="Kharagpur, West Bengal"

echo "from webapp.models import Venue; Venue.objects.create(name='$venue_name1', capacity=$venue_capacity1, address_line_1='$venue_address_line_1', address_line_2='$venue_address_line_2')" | python manage.py shell

echo "$venue_name1 created successfully."

# Create Venue 2
venue_name2="Vikramshila"
venue_capacity2="400"
venue_address_line_1="8886+RMQ, IIT Kharagpur"
venue_address_line_2="Kharagpur, West Bengal"

echo "from webapp.models import Venue; Venue.objects.create(name='$venue_name2', capacity=$venue_capacity2, address_line_1='$venue_address_line_1', address_line_2='$venue_address_line_2')" | python manage.py shell

echo "$venue_name2 created successfully."

# Define event fields
event_name1="Hackathon"
event_description1="A hackathon is a design sprint-like event in which computer programmers and others involved in software development, including graphic designers, interface designers, project managers, and others, often including domain experts, collaborate intensively on software projects."
event_name2="Competitive Programming"
event_description2="Competitive programming is a mind sport usually held over the Internet or a local network, involving participants trying to program according to provided specifications. Competitive programming is recognized and supported by several multinational software and Internet companies, such as Google and Facebook."
start_date1="2024-03-01 10:00:00"
end_date1="2024-03-02 10:00:00"
start_date2="2024-03-03 10:00:00"
end_date2="2024-03-04 10:00:00"
registration_start_date="2024-02-01 10:00:00"
registration_end_date="2024-02-28 10:00:00"
max_participants=50
min_participants=10

# Create events
echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer = Organizer.objects.get(user__username='$organizer_username'); venue = Venue.objects.get(name='$venue_name1'); event1 = Event.objects.create(name='$event_name1', description='$event_description1', start_date='$start_date1', end_date='$end_date1', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event1.organizers.add(organizer)" | python manage.py shell

echo "Event 1 created successfully. Organized by $organizer_username. Venue: $venue_name1."

# Include organizer 2 and 3 in event 2
echo "from webapp.models import Event, Venue, Organizer; from django.utils import timezone; organizer2 = Organizer.objects.get(user__username='$organizer2_username'); organizer3 = Organizer.objects.get(user__username='$organizer3_username'); venue = Venue.objects.get(name='$venue_name2'); event2 = Event.objects.create(name='$event_name2', description='$event_description2', start_date='$start_date2', end_date='$end_date2', venue=venue, registration_start_date='$registration_start_date', registration_end_date='$registration_end_date', max_participants=$max_participants, min_participants=$min_participants); event2.organizers.add(organizer2, organizer3)" | python manage.py shell

echo "Event 2 created successfully. Organized by $organizer2_username and $organizer3_username. Venue: $venue_name2."

# Create Ext Participant
username="exp"
password="exp"
organization="IIT Bombay"
email="extpar@extpar.com"
address_line_1="1234 Side St"
address_line_2="Bombay"
state="MH"
first_name="Linus"
last_name="Torvalds"
country="India"
pin_code="400076"
telephoneNumber="1234657890"
role="external_participant"

echo "from django.contrib.auth import get_user_model; from webapp.models import External_Participant; User = get_user_model(); user = User.objects.create_user('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', address_line_2='$address_line_2', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role'); External_Participant.objects.create(user=user, organization='$organization')" | python manage.py shell
echo "External Participant created successfully. Username: $username, Password: $password"

# Create 2 students
username="stud"
password="stud"
email="student@student.com"
address_line_1="1234 Main St"
state="CA"
first_name="Edsger"
last_name="Dijkstra"
country="US"
pin_code="12345"
telephoneNumber="1234567890"
role="student"
roll_number="18CS10001"
department="CSE"

echo "from django.contrib.auth import get_user_model; from webapp.models import Student; User = get_user_model(); user = User.objects.create_user('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role'); Student.objects.create(user=user, roll_number='$roll_number', department='$department')" | python manage.py shell
echo "Student created successfully. Username: $username, Password: $password"

username="stud2"
password="stud2"
email="stud@stud.com"
address_line_1="1234 Main St"
state="CA"
first_name="Donald"
last_name="Knuth"
country="US"
pin_code="12345"
telephoneNumber="1243567890"
role="student"
roll_number="18CS10002"
department="CSE"

echo "from django.contrib.auth import get_user_model; from webapp.models import Student; User = get_user_model(); user = User.objects.create_user('$username', '$email', '$password', first_name='$first_name', last_name='$last_name', address_line_1='$address_line_1', state='$state', country='$country', pin_code='$pin_code', telephoneNumber='$telephoneNumber', role='$role'); Student.objects.create(user=user, roll_number='$roll_number', department='$department')" | python manage.py shell
echo "Student 2 created successfully. Username: $username, Password: $password"

#Create 1 Organizer Key
key="a218m158k217"

echo "from webapp.models import Organizer_Key; Organizer_Key.objects.create(key='$key')" | python manage.py shell
echo "Organizer Key created successfully. Key: $key"

#Create 1 Accommodation
accomodation_name="Azad Hall"
address_line_1=" Colony Road"
address_line_2=", IIT Kharagpur, West Bengal"
cost_per_night=1000
facilities="Washroom, Bed, Common Room, Mess, Wifi, Tempo"
contact="9876543210"

echo "from webapp.models import Accomodation; Accomodation.objects.create(accomodation_name='$accomodation_name', address_line_1='$address_line_1', address_line_2='$address_line_2', cost_per_night=$cost_per_night, facilities='$facilities', contact='$contact')" | python manage.py shell

echo "Accomodation created successfully. Name: $accomodation_name"

#Create 1 Participant_Accomodation which links the external participant to the accomodation

echo "from webapp.models import External_Participant, Accomodation, Participant_Accomodation; participant = External_Participant.objects.get(user__username='exp'); accomodation = Accomodation.objects.get(accomodation_name='$accomodation_name'); Participant_Accomodation.objects.create(participant=participant, accomodation=accomodation, room_number='100')" | python manage.py shell


# Run the server
python3 manage.py runserver
