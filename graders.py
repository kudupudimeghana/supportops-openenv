import json
from typing import Any, Dict, List


def clamp_score(score: float) -> float:
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return min(max(round(float(score), 2), 0.01), 0.99)


def normalize_text(x: Any) -> str:
    return str(x).strip().lower()


def score_classification(pred: str, gold: str) -> float:
    return clamp_score(1.0 if normalize_text(pred) == normalize_text(gold) else 0.0)


def score_priority(pred: str, gold: str) -> float:
    return clamp_score(1.0 if normalize_text(pred) == normalize_text(gold) else 0.0)


def score_routing(pred: str, gold: str) -> float:
    return clamp_score(1.0 if normalize_text(pred) == normalize_text(gold) else 0.0)


def score_escalation(pred: Any, gold: Any) -> float:
    return clamp_score(1.0 if bool(pred) == bool(gold) else 0.0)


def score_reply(reply: str, required_keywords: List[str]) -> float:
    if not reply:
        return 0.01

    reply_lower = normalize_text(reply)
    keywords = required_keywords or []

    if len(keywords) == 0:
        return 0.99

    hits = sum(1 for kw in keywords if normalize_text(kw) in reply_lower)
    raw_score = hits / len(keywords)

    return clamp_score(raw_score)


def safe_task_scores(task_scores: Dict[str, float]) -> Dict[str, float]:
    return {k: clamp_score(v) for k, v in task_scores.items()}


def grade_single(prediction: Dict[str, Any], gold: Dict[str, Any]) -> Dict[str, float]:
    task_scores = {
        "classification": score_classification(
            prediction.get("classification", ""),
            gold.get("classification", "")
        ),
        "priority": score_priority(
            prediction.get("priority", ""),
            gold.get("priority", "")
        ),
        "routing": score_routing(
            prediction.get("routing", ""),
            gold.get("routing", "")
        ),
        "escalation": score_escalation(
            prediction.get("escalation", False),
            gold.get("escalation", False)
        ),
        "reply": score_reply(
            prediction.get("reply", ""),
            gold.get("required_keywords", [])
        ),
    }

    return safe_task_scores(task_scores)


def grade(prediction: Dict[str, Any], gold: Dict[str, Any]) -> Dict[str, Any]:
    task_scores = grade_single(prediction, gold)
    overall = clamp_score(sum(task_scores.values()) / len(task_scores))

    return {
        "task_scores": safe_task_scores(task_scores),
        "score": overall
    }


# Optional local test
if __name__ == "__main__":
    pred = {
        "classification": "billing",
        "priority": "high",
        "routing": "support",
        "escalation": True,
        "reply": "We are sorry. We will refund your payment and resolve the issue quickly."
    }

    gold = {
        "classification": "billing",
        "priority": "high",
        "routing": "support",
        "escalation": True,
        "required_keywords": ["sorry", "refund", "resolve"]
    }

    result = grade(pred, gold)
    print(json.dumps(result, indent=2))
