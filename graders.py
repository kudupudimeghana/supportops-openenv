def score_classification(pred: str, gold: str) -> float:
    return 1.0 if pred == gold else 0.0


def score_priority(pred: str, gold: str) -> float:
    return 1.0 if pred == gold else 0.0


def score_routing(pred: str, gold: str) -> float:
    return 1.0 if pred == gold else 0.0


def score_escalation(pred: bool, gold: bool) -> float:
    return 1.0 if pred == gold else 0.0


def score_reply(reply: str, required_keywords: list[str]) -> float:
    if not reply:
        return 0.0

    reply_lower = reply.lower()
    hits = sum(1 for kw in required_keywords if kw.lower() in reply_lower)

    return round(hits / max(1, len(required_keywords)), 2)