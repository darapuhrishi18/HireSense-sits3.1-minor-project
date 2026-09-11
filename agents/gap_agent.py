def analyze_gaps(missing_skills, score):
    drawbacks = [
        f"Missing required skill: {skill}" for skill in missing_skills
    ]

    recommendations = [
        f"Learn {skill} and build a practical project demonstrating it."
        for skill in missing_skills
    ]

    # This is an estimate for the MVP, not a guaranteed outcome.
    estimated_improvement = min(85, score + len(missing_skills) * 7)

    if score < 50:
        overall = "The resume has significant gaps compared with this job."
    elif score < 60:
        overall = "The resume has several important gaps that should be addressed."
    elif score < 75:
        overall = "The resume is reasonably aligned, but additional skills can improve it."
    else:
        overall = "The resume is strongly aligned with the detected requirements."

    return {
        "overall": overall,
        "drawbacks": drawbacks,
        "recommendations": recommendations,
        "estimated_improvement": estimated_improvement,
    }
