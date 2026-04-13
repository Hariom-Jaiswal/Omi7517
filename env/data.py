from .models import Email

def get_initial_emails(task_level: str) -> list[Email]:
    if task_level == "EASY":
        return [
            Email(id="e1", subject="Server outage", body="The production server is down. Urgent!"),
            Email(id="e2", subject="Weekly Newsletter", body="Here are the top stories of the week."),
        ]
    elif task_level == "MEDIUM":
        return [
            Email(id="e1", subject="Project sync", body="Let's schedule a meeting tomorrow at 10 AM to discuss the project."),
            Email(id="e2", subject="Bug report", body="Found a bug in the login flow. Please fix it."),
        ]
    elif task_level == "HARD":
        return [
            Email(id="e1", subject="Client escalation", body="CLIENT ANGRY! Needs meeting today at 2 PM or 3 PM!"),
            Email(id="e2", subject="Urgent bug", body="Payment gateway is failing. Critical!"),
            Email(id="e3", subject="Lunch?", body="Want to grab lunch today at 12 PM?"),
        ]
    return []
