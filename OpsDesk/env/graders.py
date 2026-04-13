from .models import State, Action
from typing import List

def grade_easy(state: State, history: List[Action]) -> float:
    score = 0.0
    classifications = {a.email_id: a.metadata.get("classification") for a in history if a.action_type == "classify_email"}
    if classifications.get("e1") == "urgent": score += 0.5
    if classifications.get("e2") == "spam": score += 0.5
    return score

def grade_medium(state: State, history: List[Action]) -> float:
    score = 0.0
    if len(state.observation.tasks) >= 1: score += 0.5
    if any(m.time == "10 AM" for m in state.observation.calendar): score += 0.5
    return score

def grade_hard(state: State, history: List[Action]) -> float:
    score = 0.0
    classifications = {a.email_id: a.metadata.get("classification") for a in history if a.action_type == "classify_email"}
    if classifications.get("e2") == "urgent": score += 0.4
    if any(m.time in ["2 PM", "3 PM"] for m in state.observation.calendar): score += 0.3
    if len(state.observation.tasks) >= 1: score += 0.3
    return score

def compute_final_score(task_level: str, state: State, action_history: List[Action]) -> float:
    if task_level == "EASY": return grade_easy(state, action_history)
    elif task_level == "MEDIUM": return grade_medium(state, action_history)
    elif task_level == "HARD": return grade_hard(state, action_history)
    return 0.0
