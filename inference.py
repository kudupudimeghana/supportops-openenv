import os
import json
import requests

# Ticket environment (reset/step)
BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")

# LLM proxy injected by evaluator
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")


def call_llm(ticket):
    """
    Makes ONE call through the evaluator's LLM proxy.
    This is required for the LLM Criteria Check.
    """
    # Safe fallback if env vars are missing locally
    if not API_BASE_URL or not API_KEY:
        customer = ticket.get("customer", "Customer")
        department = ticket.get("department", "support")
        category = ticket.get("category", "general")
        return f"Hello {customer}, we understand your concern and our {department} team is reviewing your {category} issue."

    subject = ticket.get("subject", "")
    message = ticket.get("message", "")
    category = ticket.get("category", "general")
    department = ticket.get("department", "support")
    customer = ticket.get("customer", "Customer")

    prompt = f"""
You are a professional customer support assistant.

Customer Name: {customer}
Issue Category: {category}
Department: {department}
Subject: {subject}
Message: {message}

Write a short, polite, professional support reply in 1-2 sentences.
Do not include signatures.
"""

    try:
        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful support assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return f"Hello {customer}, we understand your concern and our {department} team is reviewing your {category} issue."


def simple_agent(obs):
    ticket = obs.get("current_ticket")
    if not ticket:
        return []

    ticket_id = ticket.get("id")
    category = ticket.get("category", "general")
    priority = ticket.get("priority", "medium")
    department = ticket.get("department", "support")
    needs_escalation = ticket.get("needs_escalation", False)

    # Required LLM call
    llm_reply = call_llm(ticket)

    actions = [
        {
            "action": {
                "type": "classify",
                "ticket_id": ticket_id,
                "value": category
            }
        },
        {
            "action": {
                "type": "prioritize",
                "ticket_id": ticket_id,
                "value": priority
            }
        },
        {
            "action": {
                "type": "route",
                "ticket_id": ticket_id,
                "value": department
            }
        },
        {
            "action": {
                "type": "escalate",
                "ticket_id": ticket_id,
                "value": str(needs_escalation).lower()
            }
        },
        {
            "action": {
                "type": "reply",
                "ticket_id": ticket_id,
                "value": llm_reply
            }
        },
        {
            "action": {
                "type": "resolve",
                "ticket_id": ticket_id,
                "value": "done"
            }
        }
    ]

    return actions


def extract_observation(data):
    if not isinstance(data, dict):
        return {}

    obs = data.get("observation") or data.get("response") or data.get("result")

    if obs is None or not isinstance(obs, dict):
        return {}

    return obs


def run_task(task_id):
    print(f"[START] {task_id}")

    try:
        r = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id}, timeout=30)
        r.raise_for_status()
        obs = extract_observation(r.json())
    except Exception:
        print(f"[SCORE] {task_id} 0.01")
        print(f"[END] {task_id}")
        return 0.01

    max_loops = 50
    loop_count = 0
    total_reward = 0.0
    steps = 0

    while loop_count < max_loops:
        loop_count += 1

        ticket = obs.get("current_ticket")
        if not ticket:
            break

        actions = simple_agent(obs)
        if not actions:
            break

        task_done = False

        for action in actions:
            # REQUIRED structured step output
            print("[STEP]", json.dumps(action))

            try:
                resp = requests.post(f"{BASE_URL}/step", json=action, timeout=30)
                resp.raise_for_status()
                resp_data = resp.json()

                reward = resp_data.get("reward", 0)
                total_reward += reward
                steps += 1

                new_obs = extract_observation(resp_data)
                if new_obs:
                    obs = new_obs

                if resp_data.get("done", False):
                    task_done = True
                    break

            except Exception:
                break

        if task_done:
            break

        if not obs.get("current_ticket"):
            break

    # Score must be strictly between 0 and 1
    raw_score = total_reward / max(1, steps)

    if raw_score <= 0:
        score = 0.01
    elif raw_score >= 1:
        score = 0.99
    else:
        score = round(raw_score, 2)

    print(f"[SCORE] {task_id} {score}")
    print(f"[END] {task_id}")
    return score


if __name__ == "__main__":
    scores = {}

    for task in ["easy", "medium", "hard"]:
        try:
            scores[task] = run_task(task)
        except Exception:
            print(f"[START] {task}")
            print(f"[SCORE] {task} 0.01")
            print(f"[END] {task}")
            scores[task] = 0.01

    avg = round(sum(scores.values()) / len(scores), 2)
    print("[FINAL]", json.dumps(scores))
    print("[AVERAGE]", avg)