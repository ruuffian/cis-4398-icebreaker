import requests
from ics import Calendar, Event
import getopt, sys

# Print help message
def usage():
        print("calexport [-t <output_directory>] [-o <file_name>]")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:t:",["help", "output=", "target="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(-1)
    output = "a"
    target = "."
    # Handle command line args
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
           output = a
        elif o in ("-t", "--target"):
            target = a
        else:
            assert False, "unhandled option"
    # Destination for .ics file
    dest = target + "/" + output + ".ics"

    headers = {
        'Authorization': "Bearer {N9bjGKfycIBolbp0TbBL3cdaSWySJEbuuiwSZwfY}",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    base_url = "https://courses.ianapplebaum.com"
    api = "/syllabus/4"

    response = requests.get(base_url+api, headers=headers).json()
    events_data = response.get("events", [])

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
    with open(dest, 'w') as f:
        f.write(cal.serialize())


if __name__ == "__main__":
    main()


