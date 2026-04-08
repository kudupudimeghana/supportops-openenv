import os
import json
import requests

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")


def simple_agent(obs):
    ticket = obs.get("current_ticket")
    if not ticket:
        return []

    ticket_id = ticket.get("id")
    category = ticket.get("category", "general")
    priority = ticket.get("priority", "medium")
    department = ticket.get("department", "support")
    needs_escalation = ticket.get("needs_escalation", False)
    customer = ticket.get("customer", "Customer")

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
                "value": f"Hello {customer}, we understand your concern and our {department} team is reviewing your {category} issue."
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
        print(f"[END] {task_id}")
        return

    max_loops = 50
    loop_count = 0

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

    print(f"[END] {task_id}")


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        try:
            run_task(task)
        except Exception:
            print(f"[START] {task}")
            print(f"[END] {task}")