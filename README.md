# SupportOps OpenEnv

SupportOps OpenEnv is a **real-world AI environment** for training and evaluating agents on **customer support ticket triage**.

It simulates a structured support operations workflow where an AI agent must make correct decisions across classification, urgency, routing, escalation, response drafting, and resolution.

---

## 🚀 What this environment simulates

An AI support assistant must:

- classify support tickets
- prioritize urgency
- route tickets to the correct department
- decide whether escalation is needed
- draft a safe response
- resolve tickets correctly

This environment is designed to feel like a **real operational support system**, not a toy benchmark.

---

## 🎯 Why this is useful

Customer support triage is a real-world task used in:

- SaaS companies
- internal IT helpdesks
- billing operations
- customer success teams
- compliance / privacy request handling

This environment lets AI agents learn and be evaluated on structured decision-making in a realistic support workflow.

---

## 🌍 Why this matters

Customer support triage is a real operational workflow used in many companies.

An AI agent in this environment must behave like a useful support operations assistant by making structured decisions under real-world business constraints such as:

- urgency
- routing
- escalation
- safe response drafting
- queue handling

This makes the environment more realistic and practically useful than a toy benchmark or simple classifier.

---

## 🧠 Supported Tasks

### Easy
Handle a single customer support ticket by classifying, prioritizing, routing, replying, and resolving it correctly.

### Medium
Handle two customer support tickets with correct triage, routing, and escalation decisions.

### Hard
Handle a mixed support queue with multiple ticket types, routing decisions, escalation logic, and safe reply drafting.

---

## ⚙️ API Endpoints

### `POST /reset`
Start a new task.

Example:
```json
{
  "task_id": "easy"
}
```

### `GET /state`
View the current environment state.

### `POST /step`
Take one action in the environment.

Example:
```json
{
  "action": {
    "type": "route",
    "ticket_id": "T1",
    "value": "billing_team"
  }
}
```

---

## 🧩 Available Actions

- `classify`
- `prioritize`
- `route`
- `escalate`
- `reply`
- `resolve`

### Example Routing Values

- `billing_team`
- `tech_support`
- `product_team`
- `privacy_team`

---

## 📦 Ticket Fields

Each ticket may include:

- `category`
- `priority`
- `department`
- `sla_hours`
- `sentiment`
- `needs_escalation`

This makes the environment more realistic and easier to understand.

---

## 🏆 Reward Design (How scoring works)

The environment gives rewards step-by-step so the agent can learn from partial progress.

### Scoring

- **+1.0** → correct classification
- **+1.0** → correct priority
- **+1.0** → correct routing
- **+1.0** → correct escalation decision
- **0.0 to 1.0** → reply quality score
- **+0.5** → correct resolution

### Penalties

- **-0.5** → wrong ticket selected
- **-0.2** → invalid action

### Final Score

Each task is converted into a **0.0 to 1.0 score** for benchmarking.

---

## 🤖 Baseline Agent

A reproducible baseline agent is included in:

```bash
python inference.py
```

It demonstrates how an agent can interact with the environment step-by-step and prints scores for:

- easy
- medium
- hard

---

## ▶️ Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the environment:

```bash
python -m uvicorn app:app --reload --port 7860
```

Open interactive API docs:

```text
http://127.0.0.1:7860/docs
```

Run baseline agent:

```bash
python inference.py
```

---

## 🔍 Example Usage

### Reset Environment

```bash
curl -X POST http://127.0.0.1:7860/reset \
-H "Content-Type: application/json" \
-d "{\"task_id\":\"easy\"}"
```

---

### Get Current State

```bash
curl http://127.0.0.1:7860/state
```

---

### Take Actions

#### Classify Ticket

```json
{
  "action": {
    "type": "classify",
    "ticket_id": "T1",
    "value": "billing"
  }
}
```

#### Prioritize Ticket

```json
{
  "action": {
    "type": "prioritize",
    "ticket_id": "T1",
    "value": "high"
  }
}
```

#### Route to Department

```json
{
  "action": {
    "type": "route",
    "ticket_id": "T1",
    "value": "billing_team"
  }
}
```

#### Escalate

```json
{
  "action": {
    "type": "escalate",
    "ticket_id": "T1",
    "value": "true"
  }
}
```

#### Reply

```json
{
  "action": {
    "type": "reply",
    "ticket_id": "T1",
    "value": "Hello Asha, our billing team is reviewing your refund request."
  }
}
```

#### Resolve

```json
{
  "action": {
    "type": "resolve",
    "ticket_id": "T1",
    "value": "done"
  }
}
```

---

## 🐳 Docker

Build:

```bash
docker build -t supportops-openenv .
```

Run:

```bash
docker run -p 7860:7860 supportops-openenv
```

---

## 🤗 Hugging Face Spaces

This project is deployable as a **Docker Space** on Hugging Face.

---

## ✅ Submission Checklist

- [x] Real-world environment
- [x] OpenEnv-style API (`reset`, `state`, `step`)
- [x] Typed models
- [x] 3 tasks (easy → medium → hard)
- [x] Agent graders
- [x] Reward shaping
- [x] Baseline inference script
- [x] Dockerfile
- [x] `openenv.yaml`

---

## 📌 Summary

SupportOps OpenEnv is a structured environment for evaluating whether AI agents can behave like useful support operations assistants in a realistic ticket triage workflow.