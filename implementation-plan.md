# Guitar Lead Funnel - Implementation Plan

This document outlines the step-by-step implementation plan to build the Guitar Lead Funnel. It is based on the PRD, architecture, questionnaires, scoring logic, and result logic documents.

## Proposed Changes

We will execute the project in 7 distinct phases, separating concerns between the Backend (FastAPI), Data (Sheets), Frontend (UX), and external APIs.

---

### Phase 1: Project Setup & Backend Skeleton
**Goal:** Establish the foundation for the FastAPI backend and configure the environment.

#### `backend/main.py`
- Initialize the FastAPI application.
- Set up CORS middleware to accept frontend requests.
- Create health check endpoints.

#### `backend/requirements.txt`
- Define Python dependencies (`fastapi`, `uvicorn`, `pydantic`, `google-api-python-client`, `requests`).

#### `backend/.env`
- Set up environment variables structure for Google Credentials and email SMTP/API settings. *(Note: WhatsApp API is deferred for now).*

---

### Phase 2: Core Business Logic (Scoring & Archetypes)
**Goal:** Implement the authoritative backend logic mapped from `scoringLogic.md` and `ResultLogic.md`.

#### `backend/models/lead.py`
- Create Pydantic models to validate incoming questionnaire submissions for Ad 1, Ad 2, and Ad 3.

#### `backend/services/scoring_service.py`
- Implement the logic to assign fixed points to MCQ answers and return a total score and qualification status.

#### `backend/services/result_service.py`
- Implement the matrices to map high-signal questions (Experience, Ability, Goal, Practice) to the 12 predefined result archetypes.

#### `backend/api/routes/lead_routes.py`
- Create the `POST /lead` endpoint. It will receive frontend data, call the scoring service, call the result service, and return the exact text from `results.md`.

---

### Phase 3: Google Sheets CRM Integration
**Goal:** Set up state management and record the entire user journey.

#### `backend/services/sheets_service.py`
- Authenticate with the Google Sheets API *(Agent will guide the user through setting up Google Service Accounts)*.
- Implement the function to append a new row containing all fields defined in `architecture.md` (e.g., `lead_id`, `campaign_source`, `frontend_score`, `verified_score`, `result_archetype`).
- Integrate this service into `POST /lead` so every submission is logged.

---

### Phase 4: Frontend Development
**Goal:** Build the interactive web app containing the 3 questionnaires and result screens based on the provided design file.

#### `frontend/`
- Review the design file provided in the folder.
- Build the landing pages for the 3 distinct entry experiences.
- Implement the interactive 6-question forms.
- Build the Result Reveal screen to display the personalized archetype returned from the backend.
- Include the CTA to either book a consultation (if qualified) or receive free resources (if unqualified).

---

### Phase 5: Scheduling & Calendar Integration
**Goal:** Allow qualified leads to book available counselling slots.

#### `backend/services/calendar_service.py`
- Integrate Google Calendar API to read counsellor availability.
- Implement logic to create new events and generate Google Meet links.

#### `backend/api/routes/booking_routes.py`
- Create `GET /available-slots` to supply the frontend with bookable times.
- Create `POST /book` to finalize the booking, re-check availability, and update the existing Google Sheet row with the `meeting_date` and `meeting_link`.

---

### Phase 6: Notifications & Follow-up
**Goal:** Automate confirmation and resource delivery via Email. *(WhatsApp integration is deferred).*

#### `backend/services/email_service.py`
- Integrate Gmail API (or standard SMTP) to dispatch stylized confirmation emails and resource links.

#### `backend/api/routes/booking_routes.py` & `lead_routes.py`
- Trigger the notification services upon successful booking or unqualified lead submission.

---

### Phase 7: Deployment & Testing
**Goal:** Launch the MVP.

- **Backend:** Deploy the FastAPI server locally for initial testing, then package for deployment to Google Cloud Run or Vercel.
- **Frontend:** Deploy the Antigravity frontend to a static host (e.g., Vercel, Netlify).
- **Verification:** Perform End-to-End manual testing of all 3 ad funnels to ensure Google Sheets populates correctly, logic triggers accurately, and the correct result text is shown.
