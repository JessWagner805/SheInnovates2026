from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import torch

# Load model once (globally, so it doesn't reload on every request)
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Use GPU if available for faster inference
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def analyze_issue(issue):
    
    prompt = f"""Analyze this Jira issue for fake progress patterns.

Issue Data:
- Issue Key: {issue['issue_key']}
- Status Changes: {len(issue['status_history'])} transitions
- Story Points: {issue['story_points']}
- Days in Progress: {issue['actual_days_in_progress']} (team avg: {issue['team_avg_days']})
- Times Reopened: {issue['times_reopened']}
- Comments: {issue['comments_count']}

Status History: {issue['status_history']}

Based on this data, is there fake progress? Provide:
1. Risk assessment (high/low)
2. Risk score (0-100)
3. Brief explanation

Answer in JSON format with keys: fake_progress (boolean), risk_score (number), explanation (string)
"""

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
    
    outputs = model.generate(
        **inputs,
        max_length=200,
        num_beams=4,  # Better quality output
        early_stopping=True
    )
    
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print("RAW MODEL RESPONSE:", output_text)  # Debug

    # Try to parse JSON from response
    try:
        # FLAN-T5 sometimes adds extra text, try to find JSON
        if "{" in output_text and "}" in output_text:
            json_start = output_text.find("{")
            json_end = output_text.rfind("}") + 1
            json_str = output_text[json_start:json_end]
            parsed = json.loads(json_str)
        else:
            parsed = json.loads(output_text)
        
        # Validate required keys exist
        if "fake_progress" in parsed and "risk_score" in parsed and "explanation" in parsed:
            return parsed
        else:
            raise ValueError("Missing required keys")
            
    except Exception as e:
        print(f"Parsing error: {e}")
        
        # Fallback: create analysis from heuristics if model fails
        risk_score = 0
        
        # Simple heuristic calculation
        if issue['times_reopened'] > 0:
            risk_score += 30
        if issue['actual_days_in_progress'] > issue['team_avg_days'] * 1.5:
            risk_score += 40
        if len(issue['status_history']) > 5:
            risk_score += 20
        if issue['comments_count'] > 10:
            risk_score += 10
            
        risk_score = min(risk_score, 100)
        
        return {
            "fake_progress": risk_score > 50,
            "risk_score": risk_score,
            "explanation": f"Model parsing failed. Heuristic score based on {issue['times_reopened']} reopens and {issue['actual_days_in_progress']}/{issue['team_avg_days']} days ratio."
        }