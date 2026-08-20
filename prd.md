# Product Requirements Document: Guitar Lead Funnel

## 1. Product Overview & Objectives

The Guitar Lead Funnel is a web-based lead generation and qualification system designed to replace traditional sales forms with an interactive, value-driven "mini-product." By offering users personalized insights into their guitar-learning journey, the system automatically segments, scores, and qualifies leads for a free 15-minute consultation.

### Primary Goals:
- **Increase qualified lead capture rates** via personalized assessments.
- **Automate lead scoring** without the use of LLMs.
- **Seamlessly integrate booking** for high-scoring leads while automatically distributing resources to lower-scoring leads.

---

## 2. Target Audience

| Audience Segment | Description |
| :--- | :--- |
| **Absolute Beginners** | Users exploring the idea of playing guitar, needing foundational guidance. |
| **Self-Taught Strugglers** | Players who know basic chords but are stuck on the "YouTube plateau." |
| **Goal-Oriented Players** | Users wanting to master specific genres (e.g., Bollywood, Indie) or reach specific milestones (e.g., singing and playing). |

---

## 3. User Journey & Core Flow

1. **Traffic Acquisition:** Users enter the funnel via Meta Ads targeting three distinct angles (Learning Profile, Song Repertoire, Timeline Estimator).
2. **Assessment:** Users complete a 6-question interactive form.
3. **Processing:** The backend instantly calculates a qualification score and maps the user to a specific result archetype.
4. **Result Reveal:** The user receives a personalized action plan.
5. **Conversion:**
   - **Qualified Leads:** Prompted to book a live consultation via an integrated calendar.
   - **Unqualified Leads:** Prompted to receive free resources.
6. **Follow-up:** Automated delivery of confirmations and resources.
   > [!TIP]
   > Because WhatsApp leads are hot leads, immediate delivery of resources and scheduling confirmations via the WhatsApp Business API is a primary focus for this conversion step.

---

## 4. Functional Requirements

### 4.1. The Assessment Engine
- **Requirement:** The frontend must support three distinct entry questionnaires mapped to the Meta Ad campaigns.
- **Reference:** See [`questionnair.txt`](file:///c:/Guitar%20Lead%20Funnel/questionnair.txt) for the exact copy, questions, and multiple-choice options for Ad 1, Ad 2, and Ad 3.

### 4.2. Scoring & Qualification Logic
- **Requirement:** Every submitted answer must be assigned a fixed numerical value to calculate a total score out of 100. 
  > [!IMPORTANT]
  > The Python backend serves as the authoritative source for this calculation to prevent frontend manipulation.
- **Reference:** See [`scoringLogic.txt`](file:///c:/Guitar%20Lead%20Funnel/scoringLogic.txt) for the exact point distributions for every answer option across all three assessments.

### 4.3. Result Generation
- **Requirement:** The system must map specific combinations of high-signal answers to predefined result archetypes rather than using generative AI.
- **Reference (Mapping):** See [`ResultLogic.txt`](file:///c:/Guitar%20Lead%20Funnel/ResultLogic.txt) for the exact matrix dictating which question/option combinations trigger which archetype.
- **Reference (Copy):** See [`results.txt`](file:///c:/Guitar%20Lead%20Funnel/results.txt) for the finalized, user-facing text for all 12 variations.

### 4.4. Scheduling & CRM Integration
- **Requirement:** The platform must read live availability and write new appointments without double-booking. All user data, scores, and status updates must be logged in the MVP database.
- **Reference:** See [`architecture.md`](file:///c:/Guitar%20Lead%20Funnel/architecture.md) for the integration guidelines covering the Google Calendar API, Google Meet, and Google Sheets CRM structure.

---

## 5. Technical Architecture & Stack

| Component | Technology | Deployment Strategy |
| :--- | :--- | :--- |
| **Frontend** | Antigravity | Deployed via a static hosting provider or Vercel |
| **Backend** | Python + FastAPI | Local for MVP, scaling to Google Cloud Run or Vercel Functions |
| **Database** | Google Sheets | MVP state management |
| **Integrations** | Google Calendar API, Google Meet API, Gmail API, WhatsApp Business API | N/A |

> [!NOTE]
> See [`architecture.md`](file:///c:/Guitar%20Lead%20Funnel/architecture.md) for detailed deployment strategies and security principles (e.g., environment variable management).
