from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from backend.models.lead import BookingRequest
from backend.services.calendar_service import get_available_slots, create_booking
from backend.services.sheets_service import update_lead
from backend.services.email_service import send_booking_confirmation_email
from backend.api.limiter import limiter

router = APIRouter()

@router.get("/available-slots")
@limiter.limit("10/minute")
async def fetch_available_slots(request: Request):
    try:
        slots = get_available_slots(days=7)
        return {"slots": slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/book")
@limiter.limit("5/minute")
async def submit_booking(request: Request, submission: BookingRequest):
    try:
        # Create Google Calendar Event
        booking_info = create_booking(
            lead_name=submission.name, 
            lead_email=submission.email, 
            lead_phone=submission.phone, 
            time_slot_str=submission.time_slot
        )
        
        meet_link = booking_info.get("meet_link", "")
        meeting_date = booking_info.get("date", submission.time_slot)
        
        # Update the row in Google Sheets matching lead_id
        update_lead(
            lead_id=submission.lead_id, 
            name=submission.name, 
            phone=submission.phone, 
            time_slot=submission.time_slot,
            meeting_date=meeting_date,
            meeting_link=meet_link
        )
        
        # Send booking confirmation email
        email_sent = send_booking_confirmation_email(
            to_email=submission.email,
            lead_name=submission.name,
            time_slot=submission.time_slot,
            meet_link=meet_link
        )
        
        if not email_sent:
            print(f"Warning: Failed to send booking confirmation email to {submission.email}")
            
        # --- NEW LOGIC: Send delayed result email for hot leads ---
        from backend.services.sheets_service import get_lead, update_email_sent_status
        import json
        from backend.services.result_service import generate_result
        import os
        
        lead = get_lead(submission.lead_id)
        if lead and lead.get("email_status") != "Sent":
            raw_answers_str = lead.get("raw_answers")
            if raw_answers_str:
                try:
                    answers_dict = json.loads(raw_answers_str)
                    
                    selected_songs_str = lead.get("selected_songs", "")
                    if selected_songs_str and selected_songs_str != "None":
                        if selected_songs_str.strip().startswith("["):
                            try:
                                selected_songs = json.loads(selected_songs_str)
                            except:
                                selected_songs = []
                        else:
                            selected_songs = [s.strip("- ").strip() for s in selected_songs_str.split("\n") if s.strip()]
                    else:
                        selected_songs = []
                        
                    campaign_source = lead.get("campaign_source")
                    result_data = generate_result(campaign_source, answers_dict, selected_songs)
                    
                    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                    if result_data.get("is_beginner"):
                        attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Beginner_Roadmap.pdf")
                    else:
                        attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Intermediate_Roadmap.pdf")
                    
                    from backend.services.email_service import send_result_email
                    
                    frontend_url = os.getenv("FRONTEND_URL", "https://guitar-lead-funnel.vercel.app").rstrip("/")
                    booking_link = f"{frontend_url}/book?lead_id={submission.lead_id}&email={submission.email}"
                    result_email_sent = send_result_email(
                        to_email=submission.email, 
                        result_title=result_data["title"], 
                        result_content=result_data["content"],
                        attachment_path=attachment_path,
                        booking_link=booking_link,
                        already_booked=True,
                        selected_songs=selected_songs
                    )
                    
                    if result_email_sent:
                        update_email_sent_status(submission.lead_id)
                except Exception as ex:
                    print(f"Warning: Failed to send delayed result email: {ex}")
        # ------------------------------------------------------------
        
        return {"status": "success", "message": "Booking confirmed and CRM updated.", "meet_link": meet_link, "email_sent": email_sent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
