def generate_report(exercise, metrics):

    reps = metrics.get("reps", 0)

    score = 100
    positives = []
    improvements = []

    if "extension_status" in metrics:

        if metrics["extension_status"] == "FULL EXTENSION":
            positives.append("Full extension achieved")
        else:
            score -= 15
            improvements.append(
                "Focus on achieving full extension"
            )

    if "back_arch_status" in metrics:

        if metrics["back_arch_status"] == "Neutral":
            positives.append("Neutral back position")
        else:
            score -= 10
            improvements.append(
                "Avoid excessive back arch"
            )

    score = max(score, 0)

    return {
        "exercise": exercise,
        "reps": reps,
        "score": score,
        "positives": positives,
        "improvements": improvements
    }