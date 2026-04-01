from fastapi import FastAPI, Body
from env import SupportEnv
from models import Action

app = FastAPI(
    title="SupportOps OpenEnv",
    description="""
An interactive real-world AI environment for customer support ticket triage.

## What the agent does
The agent must:
- classify support tickets
- prioritize urgency
- route tickets to the correct department
- decide whether escalation is needed
- draft a safe reply
- resolve tickets correctly

## Available Tasks
- **easy** → one ticket
- **medium** → two tickets
- **hard** → full support queue

## Available Actions
- `classify`
- `prioritize`
- `route`
- `escalate`
- `reply`
- `resolve`

## Example Routing Values
- `billing_team`
- `tech_support`
- `product_team`
- `privacy_team`

Use `/reset`, `/state`, and `/step` to interact with the environment.
""",
    version="2.0.0"
)

env = SupportEnv(task_id="easy")


@app.get("/", summary="Environment overview")
def root():
    return {
        "message": "SupportOps OpenEnv is running",
        "description": "A real-world AI environment for customer support ticket triage.",
        "docs": "/docs",
        "tasks": {
            "easy": "Handle one support ticket",
            "medium": "Handle two support tickets",
            "hard": "Handle a full mixed support queue"
        },
        "actions": ["classify", "prioritize", "route", "escalate", "reply", "resolve"],
        "example_route_values": ["billing_team", "tech_support", "product_team", "privacy_team"]
    }


@app.post("/reset", summary="Reset the environment")
def reset(
    payload: dict = Body(
        default={},
        example={"task_id": "easy"}
    )
):
    task_id = payload.get("task_id", "easy")

    if task_id not in ["easy", "medium", "hard"]:
        task_id = "easy"

    return env.reset(task_id).model_dump()


@app.get("/state", summary="Get current environment state")
def state():
    return env.state().model_dump()


@app.post("/step", summary="Take one action in the environment")
def step(
    action: Action = Body(
        ...,
        example={
            "action": {
                "type": "route",
                "ticket_id": "T1",
                "value": "billing_team"
            }
        }
    )
):
    return env.step(action.model_dump()).model_dump()