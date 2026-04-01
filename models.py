from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel


Priority = Literal["low", "medium", "high"]
Category = Literal["billing", "technical", "feature_request", "compliance"]
Department = Literal["billing_team", "tech_support", "product_team", "privacy_team"]
Sentiment = Literal["calm", "frustrated", "angry", "serious"]


class Ticket(BaseModel):
    id: str
    customer: str
    subject: str
    message: str
    category: Category
    priority: Priority
    department: Department
    sla_hours: int
    sentiment: Sentiment
    needs_escalation: bool = False
    safe_reply_keywords: List[str]


class ActionPayload(BaseModel):
    type: Literal["classify", "prioritize", "route", "reply", "escalate", "resolve"]
    ticket_id: str
    value: Optional[str] = None


class Action(BaseModel):
    action: ActionPayload


class Observation(BaseModel):
    current_ticket: Optional[Ticket] = None
    inbox_remaining: int
    completed: List[str]
    history: List[Dict[str, Any]]
    task_id: str


class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]


class ResetResponse(BaseModel):
    observation: Observation


class StateResponse(BaseModel):
    observation: Observation