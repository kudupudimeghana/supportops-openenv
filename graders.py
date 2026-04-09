def clamp_score(score):
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return float(score)


# wherever you build final output
result = {
    "task_scores": task_scores,
    "score": overall_score
}

# 🔥 FORCE FIX EVERYTHING HERE
for k in result["task_scores"]:
    result["task_scores"][k] = clamp_score(result["task_scores"][k])

result["score"] = clamp_score(result["score"])

return result
