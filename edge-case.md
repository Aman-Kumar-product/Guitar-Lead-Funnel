# Guitar Lead Funnel - Edge Case Analysis

This document outlines potential edge cases and failure modes for the Guitar Lead Funnel project, categorized by system component. Addressing these during implementation will ensure a robust and reliable MVP.

---

## 1. Frontend & User Input

### 1.1 Incomplete or Manipulated Payload
- **Scenario:** A user bypasses frontend validation and submits an incomplete form, or modifies the POST payload to include options that don't exist.
- **Mitigation:** The FastAPI backend must use strict Pydantic models. Any request missing required fields or containing invalid options must return a `422 Unprocessable Entity` error before any scoring logic or Google Sheets API calls are made.

### 1.2 Duplicate Submissions (Spam/Accidental)
- **Scenario:** A user double-clicks the submit button, or intentionally spams the form with the same email address.
- **Mitigation:** 
  - **Frontend:** Implement a debounce/loading state on the submit button.
  - **Backend:** Check Google Sheets (or a local cache) for recent submissions from the same email/phone number to prevent duplicate CRM entries and skewed analytics.

### 1.3 Invalid Contact Information
- **Scenario:** The user provides a fake email or incorrectly formatted phone number.
- **Mitigation:** Pydantic models must use Regex validation for emails and phone numbers. If the data is invalid, prompt the user on the frontend to correct it before submission.

---

## 2. Backend Scoring & Result Logic

### 2.1 Unmapped Result Archetype (Fallback Failure)
- **Scenario:** Due to a logic update or unexpected combination, the backend cannot map the user's answers to one of the 12 predefined result archetypes in `ResultLogic.md`.
- **Mitigation:** Implement a strict "Fallback Result" for each of the 3 ad campaigns (e.g., if Ad 2 fails to map, default to "Indie Chord Builder"). The system should log a warning when a fallback is triggered.

### 2.2 Missing Campaign Source
- **Scenario:** The frontend sends a payload, but the `campaign_source` (Ad 1, 2, or 3) is missing or corrupted.
- **Mitigation:** The backend cannot score the lead without knowing the source. It must reject the request with a `400 Bad Request` or fall back to a default scoring rubric and explicitly label the `campaign_source` as "Unknown" in Google Sheets.

---

## 3. Google Sheets CRM Integration

### 3.1 Google API Rate Limits
- **Scenario:** A sudden spike in Meta Ad traffic causes the system to exceed Google Sheets API rate limits (e.g., 60 requests per user per minute).
- **Mitigation:** Wrap the Google Sheets `append_row` function in a retry mechanism with exponential backoff (using a library like `tenacity`). If it ultimately fails, log the lead data to a local fallback file to ensure no data is lost.

### 3.2 Service Account Token Expiration/Revocation
- **Scenario:** The Google Service Account credentials expire or are accidentally deleted.
- **Mitigation:** The application should catch authentication errors (`401 Unauthorized`) and trigger an immediate critical alert to the developer (via email or server logs).

---

## 4. Scheduling & Calendar API

### 4.1 The Double-Booking Race Condition
- **Scenario:** Lead A and Lead B both see 4:00 PM available. Lead A selects it. Milliseconds later, Lead B selects it.
- **Mitigation:** The `POST /book` endpoint must *re-check* the Calendar availability immediately before creating the event. If the slot is no longer available, return a `409 Conflict` and ask the user to select a new time.

### 4.2 Lead Books Multiple Consultations
- **Scenario:** A qualified lead books a slot, finishes the flow, hits "back" on their browser, and books a different slot.
- **Mitigation:** Tie calendar bookings to the unique `lead_id`. If a booking request comes in for a `lead_id` that already has a `booking_status` of "Confirmed", either reject the request or update the existing event rather than creating a second one.

---

## 5. Notifications (Email/WhatsApp)

### 5.1 Bounced Emails / API Failure
- **Scenario:** The Gmail API fails to send the confirmation or resources (due to invalid email, full inbox, or Google API outage).
- **Mitigation:** The `email_status` column in Google Sheets must accurately reflect "Failed". Do not crash the entire `/lead` or `/book` request if the email fails; return the success screen to the user, but log the email failure.

### 5.2 Deferred WhatsApp Implementation
- **Scenario:** Since WhatsApp is deferred for Phase 1, hot leads might miss their calendar invitations if they don't check their email.
- **Mitigation:** Ensure the confirmation screen on the frontend explicitly tells the user: *"Check your email for the Google Meet link. If you don't see it, check your spam folder."* This manages expectations until WhatsApp is integrated.
