def clamp_score(score: float) -> float:
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return min(max(round(score, 2), 0.01), 0.99)


def score_classification(pred: str, gold: str) -> float:
    return clamp_score(1.0 if str(pred).strip().lower() == str(gold).strip().lower() else 0.0)


def score_priority(pred: str, gold: str) -> float:
    return clamp_score(1.0 if str(pred).strip().lower() == str(gold).strip().lower() else 0.0)


def score_routing(pred: str, gold: str) -> float:
    return clamp_score(1.0 if str(pred).strip().lower() == str(gold).strip().lower() else 0.0)


def score_escalation(pred: bool, gold: bool) -> float:
    return clamp_score(1.0 if bool(pred) == bool(gold) else 0.0)


def score_reply(reply: str, required_keywords: list[str]) -> float:
    if not reply:
        return 0.01

    reply_lower = str(reply).lower().strip()
    keywords = required_keywords or []

    if len(keywords) == 0:
        return 0.99

    hits = sum(1 for kw in keywords if str(kw).lower() in reply_lower)
    raw_score = hits / len(keywords)

    return clamp_score(raw_score)
