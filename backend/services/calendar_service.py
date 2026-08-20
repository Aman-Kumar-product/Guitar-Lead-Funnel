import os
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pytz
import uuid

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

def get_calendar_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    try:
        if creds_json:
            import json
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Warning: {CREDENTIALS_FILE} not found. Calendar integration disabled.")
                return None
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Error initializing Google Calendar service: {e}")
        return None

def get_available_slots(days=7):
    """
    Returns available time slots for the next `days` days.
    For MVP, we generate some standard business hour slots and remove ones that conflict with existing events.
    """
    CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
    service = get_calendar_service()
    if not service or not CALENDAR_ID:
        # Fallback for UI testing
        return ["Monday 10:00 AM", "Tuesday 2:00 PM", "Thursday 4:30 PM"]

    try:
        timezone_str = os.getenv("TIMEZONE", "Asia/Kolkata")
        tz = pytz.timezone(timezone_str) # Configurable timezone
        now = datetime.now(tz)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=days)).isoformat()

        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Build occupied time blocks
        occupied = []
        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            if start and end:
                occupied.append((datetime.fromisoformat(start), datetime.fromisoformat(end)))

        # Generate prospective slots (e.g., 10 AM, 2 PM, 4 PM for the next few weekdays)
        available_slots = []
        for i in range(1, days + 1):
            day = now + timedelta(days=i)
            if day.weekday() >= 5: # Skip weekends for this MVP example
                continue
                
            prospective_times = [(10, 0), (10, 30), (11, 0), (11, 30), (14, 0), (14, 30), (15, 0), (15, 30), (16, 0), (16, 30)]
            for hour, minute in prospective_times:
                slot_start = day.replace(hour=hour, minute=minute, second=0, microsecond=0)
                slot_end = slot_start + timedelta(minutes=30)
                
                # Check conflict
                conflict = False
                for occ_start, occ_end in occupied:
                    if (slot_start < occ_end and slot_end > occ_start):
                        conflict = True
                        break
                
                if not conflict:
                    # Include date for uniqueness and append end time
                    formatted_slot = f"{slot_start.strftime('%A, %b %d at %I:%M %p')} - {slot_end.strftime('%I:%M %p')}"
                    available_slots.append(formatted_slot)

        return available_slots[:6] # Return max 6 slots for UI simplicity
    except Exception as e:
        print(f"Error fetching calendar slots: {e}")
        return ["Monday 10:00 AM", "Tuesday 2:00 PM", "Thursday 4:30 PM"]

def create_booking(lead_name, lead_email, lead_phone, time_slot_str):
    """
    Creates a calendar event with a Google Meet link.
    """
    CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
    service = get_calendar_service()
    if not service or not CALENDAR_ID:
        return {"meet_link": "https://meet.google.com/mock-link", "date": time_slot_str}

    try:
        # Parse time_slot_str back to datetime (Assuming format "%A, %b %d at %I:%M %p")
        # In a real robust app, time_slot would be passed as ISO datetime.
        # Since frontend sends string, we'll parse it approximately for current year.
        timezone_str = os.getenv("TIMEZONE", "Asia/Kolkata")
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        
        try:
            time_slot_str_start = time_slot_str.split(" - ")[0]
            parsed_time = datetime.strptime(time_slot_str_start, "%A, %b %d at %I:%M %p")
            # Assign current year
            slot_start = parsed_time.replace(year=now.year)
            # Handle year boundary edge case
            if slot_start < now.replace(tzinfo=None) - timedelta(days=30):
                slot_start = slot_start.replace(year=now.year + 1)
                
            slot_start = tz.localize(slot_start)
        except ValueError:
            # Fallback if string is simple like "Monday 10:00 AM" from dummy data
            slot_start = now + timedelta(days=1)
            
        slot_end = slot_start + timedelta(minutes=30)

        # Check for conflicts to prevent double booking
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=slot_start.isoformat(),
            timeMax=slot_end.isoformat(),
            singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])
        for evt in events:
            evt_start = evt['start'].get('dateTime')
            evt_end = evt['end'].get('dateTime')
            if evt_start and evt_end:
                occ_start = datetime.fromisoformat(evt_start)
                occ_end = datetime.fromisoformat(evt_end)
                if slot_start < occ_end and slot_end > occ_start:
                    raise Exception("Time slot is already booked. Please choose another one.")

        event = {
            'summary': f'Guitar Strategy Call: {lead_name}',
            'description': f'Strategy Call with {lead_name}.\nPhone: {lead_phone}\nEmail: {lead_email}',
            'start': {
                'dateTime': slot_start.isoformat(),
                'timeZone': timezone_str,
            },
            'end': {
                'dateTime': slot_end.isoformat(),
                'timeZone': timezone_str,
            }
        }

        created_event = service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()

        # Service accounts on non-Workspace domains can't generate Meet links natively.
        # We use a static link provided in .env or a default placeholder.
        static_meet_link = os.getenv("STATIC_MEET_LINK", "https://meet.google.com/your-static-link")
        meet_link = created_event.get('hangoutLink', static_meet_link)
        
        # Also update the event to include the link in the location so it's clickable
        if not created_event.get('hangoutLink'):
            service.events().patch(
                calendarId=CALENDAR_ID,
                eventId=created_event['id'],
                body={'location': static_meet_link}
            ).execute()
        
        return {
            "meet_link": meet_link,
            "date": slot_start.isoformat()
        }

    except Exception as e:
        print(f"Error creating calendar event: {e}")
        return {"meet_link": "https://meet.google.com/abc-defg-hij", "date": time_slot_str}
