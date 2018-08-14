import sys
import os
import requests
import json
from datetime import datetime
from ics import Calendar, Event

ADDRESS = '127.0.0.1'
URL = "http://{}:8000".format(ADDRESS)
URL_LOGIN = "{}/accounts/login/".format(URL)

client = requests.session()

# Retrieve the CSRF token first
client.get(URL_LOGIN) # sets cookies:
csrftoken = client.cookies['csrftoken']

# Login
login_data = {
    'username': os.environ['FTTA_USERNAME'],
    'password': os.environ['FTTA_PASSWORD'],
    'csrfmiddlewaretoken': csrftoken,
    'next': '/'
}
r = client.post(URL_LOGIN, data=login_data)

# Get events
res = client.get("{}/api/events".format(URL))

# Make Calendar
c = Calendar()

# Iterate through events
for event in res.json():
    e = Event()
    e.name = event['name']
    # Translate time format
    start_datetime = datetime.strptime(event['start_datetime'][0:-6], '%Y-%m-%dT%H:%M:%S')
    e.begin = start_datetime.strftime("%Y%m%d %H:%M:%S")
    end_datetime = datetime.strptime(event['end_datetime'][0:-6], '%Y-%m-%dT%H:%M:%S')
    e.end = end_datetime.strftime("%Y%m%d %H:%M:%S")
    c.events.add(e)

with open('training_schedule.ics', 'w') as f:
    f.writelines(c)
