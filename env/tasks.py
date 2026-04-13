from typing import Dict, Any

TASKS = {
    "EASY": {
        "description": "Classify emails correctly.",
        "expected_classifications": {"e1": "urgent", "e2": "spam"}
    },
    "MEDIUM": {
        "description": "Extract task from bug report and schedule meeting for project sync.",
        "expected_meetings": {"e1": "10 AM"}
    },
    "HARD": {
        "description": "Handle multiple conflicting emails.",
        "expected_classifications": {"e2": "urgent"},
        "expected_meetings": {"e1": ["2 PM", "3 PM"]}
    }
}

def get_task_config(task_level: str) -> Dict[str, Any]:
    return TASKS.get(task_level, TASKS["EASY"])
