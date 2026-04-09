import json
from copy import deepcopy
from models import Ticket, Observation, StepResponse, ResetResponse, StateResponse, Action
from graders import (
    score_classification,
    score_priority,
    score_routing,
    score_escalation,
    score_reply
)


def clamp_score(score: float) -> float:
    """
    Ensures every reward/score stays strictly between 0 and 1.
    """
    if score <= 0:
        return 0.01
    elif score >= 1:
        return 0.99
    return round(score, 2)


class SupportEnv:
    def __init__(self, task_id: str = "easy"):
        self.task_id = task_id
        self.all_tickets = self._load_tickets()
        self.reset(task_id)

    def _load_tickets(self):
        with open("sample_data/tickets.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Ticket(**x) for x in data]

    def _select_tickets(self, task_id):
        if task_id == "easy":
            return deepcopy(self.all_tickets[:1])
        elif task_id == "medium":
            return deepcopy(self.all_tickets[:2])
        return deepcopy(self.all_tickets)

    def _obs(self):
        return Observation(
            current_ticket=self.queue[0] if self.queue else None,
            inbox_remaining=len(self.queue),
            completed=self.completed,
            history=self.history,
            task_id=self.task_id
        )

    def reset(self, task_id: str = None):
        if task_id:
            self.task_id = task_id
        self.queue = self._select_tickets(self.task_id)
        self.completed = []
        self.history = []
        return ResetResponse(observation=self._obs())

    def state(self):
        return StateResponse(observation=self._obs())

    def step(self, action_dict):
        action = Action(**action_dict).action
        reward = 0.01
        info = {}

        if not self.queue:
            return StepResponse(
                observation=self._obs(),
                reward=0.01,
                done=True,
                info={"message": "All tickets processed"}
            )

        ticket = self.queue[0]

        if action.ticket_id != ticket.id:
            reward -= 0.5
            info["error"] = "Wrong ticket targeted"
        else:
            if action.type == "classify":
                reward += score_classification(action.value, ticket.category)
                info["classification_expected"] = ticket.category

            elif action.type == "prioritize":
                reward += score_priority(action.value, ticket.priority)
                info["priority_expected"] = ticket.priority

            elif action.type == "route":
                reward += score_routing(action.value, ticket.department)
                info["department_expected"] = ticket.department

            elif action.type == "escalate":
                pred = str(action.value).lower() == "true"
                reward += score_escalation(pred, ticket.needs_escalation)
                info["needs_escalation"] = ticket.needs_escalation

            elif action.type == "reply":
                reward += score_reply(action.value or "", ticket.safe_reply_keywords)
                info["reply_keywords"] = ticket.safe_reply_keywords

            elif action.type == "resolve":
                self.completed.append(ticket.id)
                self.queue.pop(0)
                reward += 0.5
                info["resolved"] = ticket.id

            else:
                reward -= 0.2
                info["error"] = "Unknown action type"

        reward = clamp_score(reward)

        self.history.append({
            "ticket_id": action.ticket_id,
            "action_type": action.type,
            "value": action.value,
            "reward": reward
        })

        done = len(self.queue) == 0

        return StepResponse(
            observation=self._obs(),
            reward=reward,
            done=done,
            info=info
        )