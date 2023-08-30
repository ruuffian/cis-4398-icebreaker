import requests
from ics import Calendar, Event
#using added in dates 
from datetime import datetime

#gets data from api 
headers = {
    'Authorization': "Bearer N9bjGKfycIBolbp0TbBL3cdaSWySJEbuuiwSZwfY",
    'Content-Type': "application/json",
    'Accept': "application/json"
}

#api information 
base_url = "https://courses.ianapplebaum.com"
api = "/syllabus/4"

response = requests.get(base_url + api, headers=headers).json()
events_data = response.get('events', [])

# Create a new calendar
cal = Calendar()

# Loop through events from the API and add them to the calendar
for event_data in events_data:
    event = Event()
    event.name = event_data["event_name"]
    event.begin = event_data["event_date"]
    event.description = event_data["event_description"]
    cal.events.add(event)

#identify phases and related dates
phases = [
    {"name": "Inception Phase", "date": "08/28/2023"},
    {"name": "Elaboration Phase", "date": "09/10/2023"},
    {"name": "Construction Phase", "date": "10/15/2023"}
]

# Add the phases as events to the calendar
'''
for phase in phases:
    phase_event = Event()
    phase_event.name = phase["name"]
    phase_event.begin = datetime.strptime(phase["date"], "%m/%d/%Y")
    cal.events.add(phase_event) 
'''

#print(events_data)    
#print(cal)    

# Save the calendar to a file
with open('my.ics', 'w') as f:
    f.write(str(cal))
