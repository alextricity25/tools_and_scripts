import sys
import os
import requests
import json
import datetime
import pdb
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

pdb.set_trace()
# Make Calendar
c = Calendar()

# Iterate through events
for event in res.json():
    e = Event()
    e.name = event['name']
    e.begin = event['begin_datetime']
    e.end = event['end_datetime']
    c.events.append(e)

#events = json.load(res.json()[0])
#print res.json()
