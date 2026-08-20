import requests

payload = {
    "campaign_source": "ad_1",
    "email": "ihadinspiredmyself@gmail.com",
    "assessment_answers": {
        "q1": 1, "q2": 1, "q3": 1, "q4": 1, "q5": 1, "q6": 1
    }
}
resp = requests.post("http://127.0.0.1:8000/api/lead", json=payload)
print(resp.status_code, resp.text)
