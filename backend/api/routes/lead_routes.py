from fastapi import APIRouter, HTTPException, Request
from models.lead import ScoreRequest, LeadEmailRequest, BookingRequest, SendResultRequest
from services.scoring_service import calculate_score
from services.result_service import generate_result
from services.sheets_service import append_lead, update_lead
from api.limiter import limiter

router = APIRouter()

@router.post("/score")
@limiter.limit("5/minute")
async def calculate_initial_score(request: Request, submission: ScoreRequest):
    try:
        # Calculate scores
        score_details = calculate_score(submission.campaign_source, submission.assessment_answers)
        
        # Map to archetype
        result_data = generate_result(submission.campaign_source, submission.assessment_answers, getattr(submission, "selected_songs", []))
        result_content = result_data["content"]
        
        # We only return the title and short content for the gated screen
        intro_paragraph = result_data["short_content"]

        return {
            "title": result_data["title"],
            "short_content": intro_paragraph,
            "full_content": result_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lead/{lead_id}")
@limiter.limit("10/minute")
async def fetch_lead(request: Request, lead_id: str):
    try:
        from services.sheets_service import get_lead
        lead = get_lead(lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return {
            "lead_id": lead.get("lead_id"),
            "email": lead.get("email"),
            "score_details": {
                "is_qualified": lead.get("qualification") == "Qualified"
            },
            "booking_status": lead.get("booking_status"),
            "time_slot": lead.get("preferred_timing"),
            "meeting_date": lead.get("meeting_date")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lead")
@limiter.limit("5/minute")
async def submit_email_lead(request: Request, submission: LeadEmailRequest):
    try:
        # Recalculate score/archetype server-side for safety
        score_details = calculate_score(submission.campaign_source, submission.assessment_answers)
        result_data = generate_result(submission.campaign_source, submission.assessment_answers, getattr(submission, "selected_songs", []))

        # Construct lead_data dict to match append_lead signature
        lead_data = {
            "campaign_source": submission.campaign_source,
            "name": submission.name,
            "email": str(submission.email),
            "phone": submission.phone,
            "assessment_answers": submission.assessment_answers,
            "selected_songs": getattr(submission, "selected_songs", [])
        }

        # Determine which PDF to send
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # backend dir
        if result_data.get("is_beginner"):
            attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Beginner_Roadmap.pdf")
        else:
            attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Intermediate_Roadmap.pdf")

        import uuid
        lead_id = str(uuid.uuid4())
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
        booking_link = f"{frontend_url}/book?lead_id={lead_id}&email={submission.email}"

        from services.email_service import send_result_email
        from services.sheets_service import check_if_email_booked
        
        is_qualified = score_details.get("is_qualified", False)
        already_booked = False
        email_sent = False
        
        if not is_qualified:
            email_sent = send_result_email(
                to_email=str(submission.email), 
                result_title=result_data["title"], 
                result_content=result_data["content"],
                attachment_path=attachment_path,
                booking_link=booking_link,
                already_booked=already_booked,
                is_qualified=False,
                selected_songs=getattr(submission, "selected_songs", [])
            )

        # Write to Google Sheets and get the generated lead_id
        saved_lead_id = append_lead(lead_data, score_details, result_data, email_sent=email_sent, lead_id=lead_id)
        
        if not saved_lead_id:
            print("Warning: Failed to save to Google Sheets.")

        return {
            "lead_id": lead_id,
            "email": str(submission.email),
            "score_details": score_details,
            "booking_status": "Pending",
            "result": {
                "title": result_data["title"],
                "content": result_data["content"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-results-only")
@limiter.limit("5/minute")
async def submit_send_results_only(request: Request, submission: SendResultRequest):
    try:
        from services.sheets_service import get_lead, update_email_sent_status, update_lead
        from services.result_service import generate_result
        import json
        
        lead = get_lead(submission.lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
            
        raw_answers_str = lead.get("raw_answers", "{}")
        try:
            answers_dict = json.loads(raw_answers_str) if raw_answers_str else {}
        except:
            answers_dict = {}
            
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
            
        campaign_source = lead.get("campaign_source", "")
        result_data = generate_result(campaign_source, answers_dict, selected_songs)
        
        if not result_data:
            raise HTTPException(status_code=500, detail="Failed to retrieve result data")
        
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if result_data.get("is_beginner"):
            attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Beginner_Roadmap.pdf")
        else:
            attachment_path = os.path.join(base_dir, "assets", "roadmaps", "Intermediate_Roadmap.pdf")

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
        booking_link = f"{frontend_url}/book?lead_id={submission.lead_id}&email={submission.email}"
        
        from services.email_service import send_result_email
        email_sent = send_result_email(
            to_email=str(submission.email), 
            result_title=result_data["title"], 
            result_content=result_data["content"],
            attachment_path=attachment_path,
            booking_link=booking_link,
            already_booked=False, # Since they clicked "send me results instead"
            selected_songs=selected_songs
        )
        
        if email_sent:
            update_email_sent_status(submission.lead_id)
            
        # Capture name and phone if provided
        if submission.name or submission.phone:
            update_lead(
                lead_id=submission.lead_id, 
                name=submission.name, 
                phone=submission.phone, 
                time_slot="", 
                booking_status=None # Don't override their booking status
            )
            
        return {"status": "success", "email_sent": email_sent}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
