def jira_issues():
    return [
        # low risk issue
        {
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
        },
        # high risk issue
        {
            "issue_key": "PM-216",
            "status_history": [
                ("To Do", "2024-03-01"),
                ("In Progress", "2024-03-01"),
                ("Blocked", "2024-03-05"),
                ("In Progress", "2024-03-10")
            ],
            "story_points": 8,
            "actual_days_in_progress": 9,
            "team_avg_days": 4,
            "comments_count": 14,
            "times_reopened": 2
        }
    ]
