import requests
import json
import os


API_URL = "https://www.huggingfaceapi.com/api/llm"
API_KEY = os.getenv("HF_API_KEY")

def analyze_issue(issue):
    
    prompt = f"""
You are an AI system detecting fake progress patterns in Jira.

Analyze this issue and return STRICT JSON:

{{
  "fake_progress": true or false,
  "risk_score": number between 0 and 100,
  "explanation": "short explanation"
}}

Issue Data:
{json.dumps(issue, indent=2)}
"""

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "prompt": prompt,
            "max_tokens": 300
        }
    )

    result = response.json()

    try:
        parsed = json.loads(result["text"])
        return parsed
    except:
        return {"error": "Failed to parse LLM response"}
