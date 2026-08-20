from backend.models.lead import ScoreRequest
import json

payload = {
    "campaign_source": "ad_1",
    "assessment_answers": {
        "q1": 1, "q2": 1, "q3": 1, "q4": 1, "q5": 1, "q6": 1
    }
}
try:
    req = ScoreRequest(**payload)
    print("ScoreRequest OK")
except Exception as e:
    print("ScoreRequest Error:", e)

from backend.models.lead import LeadEmailRequest
payload2 = {
    "campaign_source": "ad_1",
    "email": "test@gmail.com",
    "assessment_answers": {
        "q1": 1, "q2": 1, "q3": 1, "q4": 1, "q5": 1, "q6": 1
    }
}
try:
    req = LeadEmailRequest(**payload2)
    print("LeadEmailRequest OK")
except Exception as e:
    print("LeadEmailRequest Error:", e)
