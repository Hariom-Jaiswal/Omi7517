from .models import Action, Reward
from typing import List, Dict, Any

def compute_reward(action: Action, task_level: str, task_config: Dict[str, Any], state_history: List[Action]) -> Reward:
    for prev_action in state_history:
        if prev_action.model_dump() == action.model_dump():
            return Reward(value=-0.1, info="Repeated action")

    if action.action_type == "classify_email":
        expected = task_config.get("expected_classifications", {})
        if action.email_id in expected and action.metadata.get("classification") == expected[action.email_id]:
            return Reward(value=0.2, info="Correct classification")
        return Reward(value=-0.2, info="Incorrect classification")
            
    elif action.action_type == "extract_task":
        return Reward(value=0.3, info="Task extracted")
        
    elif action.action_type == "schedule_meeting":
        expected = task_config.get("expected_meetings", {})
        if action.email_id in expected:
            expected_time = expected[action.email_id]
            chosen_time = action.metadata.get("meeting_time", "")
            if (isinstance(expected_time, list) and chosen_time in expected_time) or chosen_time == expected_time:
                return Reward(value=0.3, info="Correct scheduling")
            return Reward(value=-0.2, info="Incorrect meeting time")
        return Reward(value=-0.2, info="Scheduled meeting for wrong email")
            
    elif action.action_type in ["reply_email", "ignore_email"]:
        return Reward(value=0.1, info="Action processed")
        
    return Reward(value=-0.2, info="Unknown action")
