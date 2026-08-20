import os
import sys

# Add the backend directory to the path so we can import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from dotenv import load_dotenv
load_dotenv(override=True, dotenv_path=".env")

from services.calendar_service import get_available_slots

try:
    print("Testing Google Calendar Integration...")
    print(f"Calendar ID: {os.getenv('GOOGLE_CALENDAR_ID')}")
    slots = get_available_slots(days=7)
    print("Available Slots:", slots)
except Exception as e:
    print(f"Error: {e}")
