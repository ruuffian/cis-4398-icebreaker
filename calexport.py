import filecmp
import requests
from ics import Calendar, Event
import datetime
import os
import argparse


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
        'Authorization': "Bearer {N9bjGKfycIBolbp0TbBL3cdaSWySJEbuuiwSZwfY}",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    base_url = "https://courses.ianapplebaum.com"
    api = "/syllabus/4"

    response = requests.get(base_url + api, headers=headers)
    data = response.json()

    events_data = data.get('events', [])

    # Create a new calendar
    cal = Calendar()

    current_time = datetime.datetime.now()

    # Loop through events and add them to the calendar
    for event_data in events_data:
        event = Event()
        event.name = event_data["event_name"]
        event.begin = event_data['event_date']
        event.description = event_data["event_description"]
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
