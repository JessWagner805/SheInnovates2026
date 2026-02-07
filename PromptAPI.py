import requests
import json

API_URL = "https://www.huggingfaceapi.com/api/llm"
API_KEY = "YOUR_HF_API_KEY"  # put your key here

prompt = f"""
You are an AI assistant helping product managers detect fake progress in Jira.

Analyze the following Jira issue activity and determine:
1. Whether this issue shows signs of fake progress
2. A fake progress risk score from 0–100
3. A short explanation

Jira Issue Data:
{json.dumps(jira_issue, indent=2)}

Respond in this format:
Fake Progress: YES or NO
Risk Score: <number>
Explanation: <short explanation>
"""

response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "prompt": prompt,
        "max_tokens": 200
    }
)

result = response.json()
print(result["text"]) 
