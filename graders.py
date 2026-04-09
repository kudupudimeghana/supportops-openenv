def clamp_score(score: float) -> float:
    """
    Ensures score is strictly between 0 and 1.
    """
    if score <= 0:
        return 0.01
    elif score >= 1:
        return 0.99
    return min(max(round(score, 2), 0.01), 0.99)


def score_classification(pred: str, gold: str) -> float:
    return clamp_score(1.0 if pred.strip().lower() == gold.strip().lower() else 0.0)


def score_priority(pred: str, gold: str) -> float:
    return clamp_score(1.0 if pred.strip().lower() == gold.strip().lower() else 0.0)


def score_routing(pred: str, gold: str) -> float:
    return clamp_score(1.0 if pred.strip().lower() == gold.strip().lower() else 0.0)


def score_escalation(pred: bool, gold: bool) -> float:
    return clamp_score(1.0 if pred == gold else 0.0)


def score_reply(reply: str, required_keywords: list[str]) -> float:
    if not reply:
        return 0.01

    reply_lower = reply.lower().strip()
    hits = sum(1 for kw in required_keywords if kw.lower() in reply_lower)

    raw_score = hits / max(1, len(required_keywords))
    return clamp_score(raw_score)
