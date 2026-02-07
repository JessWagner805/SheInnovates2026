from flask import Flask, render_template
from MockJira import jira_issue
from PromptAPI import analyze_issue

app = Flask(__name__)

@app.route("/")
def index():
    issue = jira_issue()
    analysis = analyze_issue(issue)

    return render_template(
        "index.html",
        issue=issue,
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)
