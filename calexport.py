import filecmp
import requests
import datetime
import os
import argparse
from ics import Calendar, Event
from dotenv import load_dotenv
import pytz


load_dotenv()
#environment varibales


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
API = os.getenv("API")



def writeToCalendarFile(filename, calendar):
    with open(filename, 'w') as f:
        f.writelines(calendar.serialize_iter())
        calendar.serialize()
        f.close()

def get_opts():
    parser = argparse.ArgumentParser(
        prog="calexport",
        description="A simple script to export CIS 4398 events to an importable .ics file",
        )
    parser.add_argument("filename", help="name of the .ics file")
    parser.add_argument("-t", "--target", help="directory to create the file in (default: ./)", dest="target")
    return parser.parse_args()

def main():
    args = get_opts()
    # Extract filename from arguments
    name = args.filename
    target = args.target if args.target != None else "."
    destination = target + "/" + name + ".ics"

    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    base_url = BASE_URL
    api = API

    response = requests.get(base_url + api, headers=headers)
    data = response.json()

    events_data = data.get('events', [])

    # Create a new calendar
    cal = Calendar()

    current_time = datetime.datetime.now()
    
    # Making dates offset aware, ready to compare later
    utc=pytz.UTC 
    
    # Defining Project Phases names and thier date ranges
    phase_list = [
    {"name": "Inception Phase", "date": ("08/28/2023", "09/09/2023")},
    {"name": "Elaboration Phase", "date": ("09/10/2023", "10/14/2023")},
    {"name": "Construction Phase", "date": ("10/15/2023", "12/17/2023")}
    ]
    

    # Loop through events and add them to the calendar
    for event_data in events_data:
        event = Event()
        event.name = event_data["event_name"]
        event.begin = event_data['event_date']
        event.description = event_data["event_description"]
        
        # Lopp through event dates, set location to correct phase 
        for phase in phase_list:
            start_date = datetime.datetime.strptime(phase["date"][0], "%m/%d/%Y")
            #end_date = datetime.datetime.strptime(phase["date"][1], "%m/%d/%Y")
            start_date = utc.localize(start_date)
            end_date = datetime.datetime.strptime(phase["date"][1], "%m/%d/%Y")
            end_date = utc.localize(end_date)
            
            # Checking if event date falls within range
            if start_date <= event.begin <= end_date:
                event.location = phase["name"]
                break 
        
        cal.events.add(event)

    # Export the calendar to a file
    # First time this is run, create a base to compare to in the future
    try:
        if not os.path.exists('base.ics'):
            writeToCalendarFile(destination, cal)
            writeToCalendarFile('base.ics', cal)

        # if the base file exists, create a new file and compare it to the base
        else:
            writeToCalendarFile(destination, cal)
            isSame = filecmp.cmp('base.ics', destination, shallow=False)
            # if the base is not the same as the new file:
            # remove the old base
            # rename the new base
            # send an email notification
            if not isSame:
                writeToCalendarFile("base.ics", cal)
                print("The calendar has changed!")
                # Send an email notification

            else:
                print("Same calendar :)")

    except UnicodeEncodeError:
        print("In error")
        pass

if __name__ == "__main__":
    main()
