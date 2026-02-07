#this results in a high risk Fake progress report
# def jira_issue():
#     return {
#     "issue_key": "PM-214",
#     "status_history": [
#         ("To Do", "2024-03-01"),
#         ("In Progress", "2024-03-02"),
#         ("Review", "2024-03-05"),
#         ("In Progress", "2024-03-06"),
#         ("Done", "2024-03-08"),
#         ("Reopened", "2024-03-09"),
#         ("In Progress", "2024-03-10")
#     ],
#     "story_points": 5,
#     "actual_days_in_progress": 9,
#     "team_avg_days": 4,
#     "comments_count": 14,
#     "times_reopened": 1
# }

#this results in a low risk fake progress report
def jira_issue():
    return {
    "issue_key": "PM-215",
    "status_history": [
        ("To Do", "2024-03-01"),
        ("In Progress", "2024-03-02"),
        ("Review", "2024-03-04"),
        ("Done", "2024-03-05")
    ],
    "story_points": 5,
    "actual_days_in_progress": 3,
    "team_avg_days": 4,
    "comments_count": 4,
    "times_reopened": 0
}