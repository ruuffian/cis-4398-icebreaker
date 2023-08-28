import requests
from ics import Calendar, Event

headers = {
    'Authorization': "Bearer {N9bjGKfycIBolbp0TbBL3cdaSWySJEbuuiwSZwfY}",
    'Content-Type': "application/json",
    'Accept': "application/json"
}

base_url = "https://courses.ianapplebaum.com"
api = "/syllabus/4"

response = requests.get(base_url+api, headers=headers).json()
events_data = response.get('events', [])

# Create a new calendar
cal = Calendar()

# Loop through events and add them to the calendar
for event_data in events_data:
    event = Event()
    event.name = event_data["event_name"]
    event.begin = event_data["event_date"]
    event.description = event_data["event_description"]
    cal.events.add(event)

# Save the calendar to a file
with open('my.ics', 'w') as f:
    f.write(str(cal))