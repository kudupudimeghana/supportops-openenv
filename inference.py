import os
import requests

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")


def simple_agent(obs):
    ticket = obs.get("current_ticket")
    if not ticket:
        return None

    ticket_id = ticket["id"]
    category = ticket["category"]
    priority = ticket["priority"]
    department = ticket["department"]
    needs_escalation = ticket["needs_escalation"]

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
                "value": f"Hello {ticket['customer']}, we understand your concern and our {department} is reviewing your {category} issue."
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


def run_task(task_id):
    print(f"\n{'=' * 60}")
    print(f"🚀 Running task: {task_id.upper()}")
    print(f"{'=' * 60}")

    r = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id})
    obs = r.json()["observation"]

    total_reward = 0.0
    steps = 0

    while True:
        ticket = obs.get("current_ticket")
        if not ticket:
            break

        print("\n" + "-" * 60)
        print(f"📩 Ticket ID      : {ticket['id']}")
        print(f"👤 Customer       : {ticket['customer']}")
        print(f"📝 Subject        : {ticket['subject']}")
        print(f"💬 Message        : {ticket['message']}")
        print(f"🏷️ Category       : {ticket['category']}")
        print(f"⚡ Priority       : {ticket['priority']}")
        print(f"🏢 Department     : {ticket['department']}")
        print(f"⏱️ SLA            : {ticket['sla_hours']} hours")
        print(f"🙂 Sentiment      : {ticket['sentiment']}")
        print("-" * 60)

        actions = simple_agent(obs)
        if not actions:
            break

        for action in actions:
            print(f"\n➡️ Action Taken   : {action['action']['type']} = {action['action']['value']}")
            resp = requests.post(f"{BASE_URL}/step", json=action).json()
            reward = resp["reward"]
            total_reward += reward
            steps += 1
            obs = resp["observation"]

            print(f"🎯 Reward         : {reward}")
            print(f"ℹ️ Info           : {resp['info']}")

            if resp["done"]:
                break

        if not obs["current_ticket"]:
            break

    score = round(min(1.0, total_reward / max(1, steps)), 2)
    print(f"\n✅ Task {task_id} final score: {score}")
    return score


if __name__ == "__main__":
    scores = {}
    for task in ["easy", "medium", "hard"]:
        scores[task] = run_task(task)

    avg = round(sum(scores.values()) / len(scores), 2)

    print(f"\n{'=' * 60}")
    print("🏁 FINAL SCORES")
    print(f"{'=' * 60}")
    print(scores)
    print(f"📊 Average Score  : {avg}")