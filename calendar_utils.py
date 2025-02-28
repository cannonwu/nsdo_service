from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote

def create_google_calendar_link(title, start_time, end_time, details, location):
    """Generate a Google Calendar event link."""
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    params = {
        "text": title,
        "dates": f"{start_time}/{end_time}",
        "details": details,
        "location": location
    }
    query_string = "&".join([f"{key}={quote(value)}" for key, value in params.items()])
    return f"{base_url}&{query_string}"

def create_ics_file(title, start_time, end_time, location, details):
    """Generate an ICS file content."""
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{start_time}
DTEND:{end_time}
LOCATION:{location}
DESCRIPTION:{details}
END:VEVENT
END:VCALENDAR"""
    return ics_content

def generate_calendar_links(appointment_date, appointment_time):
    """Generate Google Calendar link and ICS file content."""
    # Define the local timezone (update if needed)
    local_tz = ZoneInfo("America/Los_Angeles")
    
    # Parse the appointment time as a datetime in the local timezone
    start_dt = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M").replace(tzinfo=local_tz)
    end_dt = start_dt + timedelta(hours=1)

    # Convert to UTC for Google Calendar (which expects UTC times with 'Z' suffix)
    start_dt_utc = start_dt.astimezone(ZoneInfo("UTC"))
    end_dt_utc = end_dt.astimezone(ZoneInfo("UTC"))

    # Format times for Google Calendar using UTC times
    start_time_google = start_dt_utc.strftime("%Y%m%dT%H%M%SZ")
    end_time_google = end_dt_utc.strftime("%Y%m%dT%H%M%SZ")

    # For ICS files:
    start_time_ics = start_dt.strftime("%Y%m%dT%H%M%S")
    end_time_ics = end_dt.strftime("%Y%m%dT%H%M%S")

    event_title = "Appointment at NuSmile Dental & Orthodontics"
    event_location = "1319 Blossom Hill Rd, San Jose, CA 95118"
    event_details = "Call/Text (408) 266-2800 for questions. We look forward to your visit!"

    google_calendar_link = create_google_calendar_link(event_title, start_time_google, end_time_google, event_details, event_location)
    ics_content = create_ics_file(event_title, start_time_ics, end_time_ics, event_location, event_details)

    return google_calendar_link, ics_content
