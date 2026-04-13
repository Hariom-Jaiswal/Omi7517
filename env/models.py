from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class Email(BaseModel):
    id: str
    subject: str
    body: str

class TaskItem(BaseModel):
    id: str
    description: str
    status: Literal["pending", "completed"] = "pending"

class CalendarEvent(BaseModel):
    id: str
    title: str
    time: str

class Observation(BaseModel):
    inbox: List[Email]
    tasks: List[TaskItem]
    calendar: List[CalendarEvent]

class Action(BaseModel):
    action_type: Literal["classify_email", "extract_task", "schedule_meeting", "reply_email", "ignore_email"]
    email_id: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Reward(BaseModel):
    value: float
    info: str

class State(BaseModel):
    observation: Observation
    terminated: bool
    step_count: int
    total_reward: float
