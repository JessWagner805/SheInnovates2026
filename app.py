from flask import Flask, render_template
from MockJira import jira_issues
from PromptAPI import analyze_issue

app = Flask(__name__)   # ← MUST be before @app.route


@app.route("/")
def index():
    issues = jira_issues()

    items = []
    for issue in issues:
        items.append({
            "issue": issue,
            "analysis": analyze_issue(issue)
        })

    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
