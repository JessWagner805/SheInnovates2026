from flask import Flask, render_template
from jira_mock import get_mock_jira_issue
from llm_analyzer import analyze_issue
from dotenv import load_dotenv
import os 

load_dotenv()
API_KEY = os.getenv("HF_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    issue = get_mock_jira_issue()
    analysis = analyze_issue(issue)

    return render_template(
        "index.html",
        issue=issue,
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)
