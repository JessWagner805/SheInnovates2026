# Jira Progress Auditor
*By: Pearl Singer and Jess Wagner*

### Table of Contents
- [PNC Challenge Statement](#PNC-Challenge-Statement)
- [Problem](#Problem)
- [Solution](#Solution)
- [How it Works](#How-it-Works)
- [Outcome](#Outcome)
- [Video Demonstration](#Video-Demonstration)
- [Devpost Submission](#Devpost-Submission)


## PNC Challenge Statement
*We challenge you to design an AI-powered productivity solution for Product Managers*

## Problem
Product managers rely on tools like Jira to track progress, but task activity does not always reflect real progress. Product managers are forced to trust that updates accurately represent work being completed, even when timelines and deadlines are at risk.

This creates opportunities for “fake progress,” such as:
* Tasks being marked Done and later reopened
* Excessive status changes without completion
* Creating and deleting tasks without any meaningful output
* Consistently overestimating or underestimating story points
* Prolonged time spent In Progress with little forward movement

As a result, PMs often discover problems too late, when deadlines are already missed and recovery options are limited.

## Solution

## How it works
**MockJira.py** simulates Jira issue data. **app.py** retrieves this data and sends each issue to **PromptAPI.py**, which uses the FLAN-T5 Base LLM to analyze the issue and compute a fake-progress risk score. **app.py** then combines the raw issue data with the analysis results and serves them to **index.html**, which formats and displays the information on a local web page at [http://localhost:5000/](http://localhost:5000/) when the server is running.

## Outcome

## Video Demonstration

## Devpost Submission




##Things you will need to install for this to work
pip install transformers torch flask python-dotenv
pip install -U sentence-transformers      
