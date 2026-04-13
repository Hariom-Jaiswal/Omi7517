import uuid
from typing import Tuple, Dict, Any

from .models import Observation, Action, Reward, State, TaskItem, CalendarEvent
from .data import get_initial_emails
from .tasks import get_task_config
from .rewards import compute_reward
from .graders import compute_final_score

class OpsDeskEnv:
    def __init__(self, task_level: str = "EASY", max_steps: int = 15):
        self.task_level = task_level
        self.max_steps = max_steps
        self.task_config = get_task_config(task_level)
        self.reset()
        
    def reset(self) -> Observation:
        self.step_count = 0
        self.total_reward = 0.0
        self.action_history = []
        
        self.observation = Observation(
            inbox=get_initial_emails(self.task_level),
            tasks=[],
            calendar=[]
        )
        self.terminated = False
        return self.observation
        
    def state(self) -> State:
        return State(
            observation=self.observation,
            terminated=self.terminated,
            step_count=self.step_count,
            total_reward=self.total_reward
        )
        
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        if self.terminated:
            return self.observation, Reward(value=0.0, info="Environment terminated"), True, {}
            
        reward = compute_reward(action, self.task_level, self.task_config, self.action_history)
        self.total_reward += reward.value
        
        if action.action_type == "extract_task":
            desc = action.metadata.get("task_description", "New Task")
            self.observation.tasks.append(TaskItem(id=str(uuid.uuid4())[:8], description=desc))
            
        elif action.action_type == "schedule_meeting":
            time = action.metadata.get("meeting_time", "TBD")
            self.observation.calendar.append(CalendarEvent(id=str(uuid.uuid4())[:8], title=f"Meeting: {action.email_id}", time=time))
            
        elif action.action_type in ["reply_email", "ignore_email"]:
            self.observation.inbox = [e for e in self.observation.inbox if e.id != action.email_id]
            
        self.action_history.append(action)
        self.step_count += 1
        
        if self.step_count >= self.max_steps or len(self.observation.inbox) == 0:
            self.terminated = True
            
        info = {
            "score": compute_final_score(self.task_level, self.state(), self.action_history) if self.terminated else 0.0
        }
            
        return self.observation, reward, self.terminated, info
