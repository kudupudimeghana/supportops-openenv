from fastapi import FastAPI, Body
from typing import Optional
from env import SupportEnv
from models import Action

app = FastAPI(
    title="SupportOps OpenEnv",
    description="A real-world AI environment for customer support ticket triage.",
    version="1.0.0"
)

env = SupportEnv(task_id="easy")


@app.get("/")
def root():
    return {
        "message": "SupportOps OpenEnv is running",
        "tasks": ["easy", "medium", "hard"],
        "actions": ["classify", "prioritize", "route", "escalate", "reply", "resolve"]
    }


@app.post("/reset")
def reset(payload: Optional[dict] = Body(default=None)):
    task_id = "easy"

    if payload and isinstance(payload, dict):
        task_id = payload.get("task_id", "easy")

    if task_id not in ["easy", "medium", "hard"]:
        task_id = "easy"

    return env.reset(task_id).model_dump()


@app.get("/state")
def state():
    return env.state().model_dump()


@app.post("/step")
def step(action: Action):
    return env.step(action.model_dump()).model_dump()