import os
import json
import uuid
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from data.questions import ad_campaigns

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", os.path.join(BASE_DIR, "credentials.json"))
if not os.path.isabs(CREDENTIALS_FILE):
    CREDENTIALS_FILE = os.path.join(BASE_DIR, CREDENTIALS_FILE)

HEADERS = [
    "lead_id", "created_at", "campaign_source", "name", "email", 
    "phone", "assessment_answers", "frontend_score", "verified_score", 
    "result_archetype", "qualification", "preferred_timing", "booking_status", 
    "meeting_date", "meeting_link", "resource_status", "email_status", "whatsapp_status", "raw_answers", "selected_songs"
]

def get_sheets_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    try:
        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Warning: {CREDENTIALS_FILE} not found. Sheets integration disabled.")
                return None
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error initializing Google Sheets service: {e}")
        return None

def setup_headers():
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    service = get_sheets_service()
    if not service or not SPREADSHEET_ID:
        return
    
    try:
        # Check if headers exist by reading row 1
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A1:T1").execute()
        values = result.get('values', [])
        
        if not values:
            # Sheet is empty, add headers
            body = {'values': [HEADERS]}
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID, 
                range="A1",
                valueInputOption="RAW", 
                body=body
            ).execute()
            print("Successfully initialized Google Sheets headers.")
    except Exception as e:
        print(f"Error setting up headers: {e}")

def append_lead(lead_data: dict, score_details: dict, result_data: dict, email_sent: bool = False, lead_id: str = None):
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    service = get_sheets_service()
    if not service or not SPREADSHEET_ID:
        return None
        
    try:
        # Generate unique lead ID and timestamp
        if not lead_id:
            lead_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        # Format assessment answers into bullet points
        answers_dict = lead_data.get("assessment_answers", {})
        campaign_source = lead_data.get("campaign_source", "")
        
        if isinstance(answers_dict, dict):
            answers_list = []
            campaign_data = ad_campaigns.get(campaign_source, {})
            for k, v in answers_dict.items():
                label = campaign_data.get(k, {}).get(v, str(v))
                answers_list.append(f"- {k}: {v} - {label}")
            answers_str = "\n".join(answers_list)
        else:
            answers_str = str(answers_dict)

        # Format selected songs into bullet points
        selected_songs = lead_data.get("selected_songs", [])
        if isinstance(selected_songs, list) and selected_songs:
            songs_str = "\n".join([f"- {song}" for song in selected_songs])
        else:
            songs_str = "None"
            
        # Format phone number to prevent formula errors in Sheets
        phone_val = lead_data.get("phone", "")
        if phone_val and phone_val.startswith("+"):
            phone_val = f"'{phone_val}"

        # Prepare the row data aligning with HEADERS
        row = [
            lead_id,
            created_at,
            lead_data.get("campaign_source", ""),
            lead_data.get("name", ""),
            lead_data.get("email", ""),
            phone_val,
            answers_str,
            "", # frontend_score
            score_details.get("total_score", 0),
            result_data.get("title", ""),
            "Qualified" if score_details.get("is_qualified") else "Unqualified",
            "", # preferred_timing
            "Pending", # booking_status
            "", # meeting_date
            "", # meeting_link
            "Pending" if not score_details.get("is_qualified") else "N/A", # resource_status
            "Sent" if email_sent else "Pending", # email_status
            "Pending", # whatsapp_status
            json.dumps(lead_data.get("assessment_answers", {})), # raw_answers
            songs_str # selected_songs
        ]
        
        body = {'values': [row]}
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="A:T",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        return lead_id
    except Exception as e:
        print(f"Error appending row to Google Sheets: {e}")
        return None

def update_lead(lead_id: str, name: str, phone: str, time_slot: str, meeting_date: str = "", meeting_link: str = "", booking_status: str = "Booked"):
    """
    Finds a row by lead_id and updates its Name, Phone, and Time Slot columns, as well as meeting details.
    """
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    try:
        service = get_sheets_service()
        if not service:
            return None

        # Fetch the entire sheet to find the row index
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="A:A" # Only fetch the first column (Lead ID)
        ).execute()

        values = result.get('values', [])
        
        row_index = -1
        for i, row in enumerate(values):
            if row and row[0] == lead_id:
                row_index = i + 1 # 1-indexed for Sheets
                break
                
        if row_index == -1:
            raise Exception(f"Lead ID {lead_id} not found in CRM.")

        # Prevent formula error for phone
        phone_val = phone
        if phone_val and phone_val.startswith("+"):
            phone_val = f"'{phone_val}"

        # Update columns: D (Name), F (Phone), L (preferred_timing), M, N, O
        update_data = [
            {
                "range": f"D{row_index}",
                "values": [[name]]
            },
            {
                "range": f"F{row_index}",
                "values": [[phone_val]]
            },
            {
                "range": f"L{row_index}",
                "values": [[time_slot]]
            },
            {
                "range": f"N{row_index}",
                "values": [[meeting_date]]
            },
            {
                "range": f"O{row_index}",
                "values": [[meeting_link]]
            }
        ]
        
        if booking_status is not None:
            update_data.append({
                "range": f"M{row_index}",
                "values": [[booking_status]]
            })

        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': update_data
        }

        result = sheet.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()

        return result
    except Exception as e:
        print(f"Error updating sheet: {e}")
        return None

def get_lead(lead_id: str):
    """
    Fetches a lead from Google Sheets by lead_id.
    Returns a dictionary of lead data matching HEADERS, or None if not found.
    """
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    if not SPREADSHEET_ID:
        return None
        
    try:
        service = get_sheets_service()
        if not service:
            return None
            
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="A:T"
        ).execute()
        
        values = result.get('values', [])
        for row in values:
            if row and row[0] == lead_id:
                lead_data = {}
                for i, header in enumerate(HEADERS):
                    lead_data[header] = row[i] if i < len(row) else ""
                return lead_data
                
        return None
    except Exception as e:
        print(f"Error fetching lead: {e}")
        return None

def check_if_email_booked(email: str) -> bool:
    """
    Checks if a lead with the given email already has a booking_status of 'Booked'.
    """
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    if not SPREADSHEET_ID:
        return False
        
    try:
        service = get_sheets_service()
        if not service:
            return False
            
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="E:M" # Fetch columns E (email) to M (booking_status)
        ).execute()
        
        values = result.get('values', [])
        # E is index 0, M is index 8 of the returned slice
        for row in values:
            if len(row) > 8:
                row_email = row[0]
                row_status = row[8]
                if row_email.lower() == email.lower() and row_status == "Booked":
                    return True
                    
        return False
    except Exception as e:
        print(f"Error checking email booking status: {e}")
        return False

def update_email_sent_status(lead_id: str):
    """
    Updates the email_status column (Q) to 'Sent' for a given lead_id.
    """
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    try:
        service = get_sheets_service()
        if not service:
            return None

        # Fetch the entire sheet to find the row index
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="A:A" # Only fetch the first column (Lead ID)
        ).execute()

        values = result.get('values', [])
        
        row_index = -1
        for i, row in enumerate(values):
            if row and row[0] == lead_id:
                row_index = i + 1 # 1-indexed for Sheets
                break
                
        if row_index == -1:
            raise Exception(f"Lead ID {lead_id} not found in CRM.")

        # Update column: Q (email_status)
        update_data = [
            {
                "range": f"Q{row_index}",
                "values": [["Sent"]]
            }
        ]

        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': update_data
        }

        result = sheet.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()

        return result
    except Exception as e:
        print(f"Error updating email status: {e}")
        return None
