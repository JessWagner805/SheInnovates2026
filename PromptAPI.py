import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://www.huggingfaceapi.com/api/llm"


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

    print("RAW API RESPONSE:", result)  # temporary debug

    output_text = result.get("text") or result.get("generated_text")

    try:
        parsed = json.loads(output_text)
        return parsed
    except:
        return {
            "fake_progress": False,
            "risk_score": 0,
            "explanation": "LLM response could not be parsed."
        }

