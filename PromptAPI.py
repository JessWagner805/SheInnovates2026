from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# load model once
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)



# calcuate risk score based on data from Jira issue
def calculate_risk(issue):
    """
    Deterministic risk scoring based on behavioral signals
    """
    score = 0

    # Reopenings are strong indicators
    if issue["times_reopened"] > 0:
        score += min(issue["times_reopened"] * 15, 30)

    # Time in progress vs team average
    if issue["actual_days_in_progress"] > issue["team_avg_days"] * 1.5:
        score += 40

    # Excessive status churn
    if len(issue["status_history"]) > 5:
        score += 20

    # High comment volume suggests friction
    if issue["comments_count"] > 10:
        score += 10

    score = min(score, 100)

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return score, level



# helper function for prompting the LLM
def build_explanation_draft(issue):
    """
    Builds a concrete, factual explanation draft with no AI involved
    """
    parts = []

    if issue["actual_days_in_progress"] > issue["team_avg_days"]:
        parts.append(
            f"the issue spent {issue['actual_days_in_progress']} days in progress "
            f"compared to a team average of {issue['team_avg_days']}"
        )

    if issue["times_reopened"] > 0:
        parts.append(f"it was reopened {issue['times_reopened']} times")

    if len(issue["status_history"]) > 5:
        parts.append(
            f"it experienced {len(issue['status_history'])} status transitions"
        )

    if issue["comments_count"] > 10:
        parts.append(f"it accumulated {issue['comments_count']} comments")

    if not parts:
        return (
            f"The issue spent {issue['actual_days_in_progress']} days in progress "
            f"with no reopenings or excessive status changes."
        )

    return " and ".join(parts) + "."



# feed prompt to LLM and return LLM-generated explanation
def polish_explanation_with_llm(draft):
    """
    Uses the LLM only to rewrite a known-good draft explanation
    """
    prompt = f"""
    Rewrite the following sentence to sound clear and professional for a Product Manager.

    Text:
    "{draft}"

    Rules:
    - Keep the meaning exactly the same
    - Maximum 2 sentences
    - Do not add new information
    - Do not use the words "risk", "high", "medium", "low", "fake", or "resolved"
    """

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    outputs = model.generate(
        **inputs,
        max_length=60,
        num_beams=4,
        no_repeat_ngram_size=4,
        repetition_penalty=1.4,
        early_stopping=True
    )

    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return explanation



# main function to analyze a Jira issue and return risk assessment and LLM-generated explanation
def analyze_issue(issue):
    score, level = calculate_risk(issue)
    draft = build_explanation_draft(issue)

    try:
        explanation = polish_explanation_with_llm(draft)
    except Exception:
        explanation = draft

    return {
        "fake_progress": level == "High",
        "risk_level": level,
        "risk_score": score,
        "explanation": explanation
    }