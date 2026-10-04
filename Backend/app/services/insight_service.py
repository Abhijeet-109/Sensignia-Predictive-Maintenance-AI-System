def generate_insight(condition: str, health_score: float):
    if condition == "Healthy":
        return {
            "severity": "Low",
            "message": "Machine is operating in a healthy condition."
        }

    if health_score < 20:
        severity = "Critical"
    elif health_score < 50:
        severity = "Warning"
    else:
        severity = "Attention"

    return {
        "severity": severity,
        "message": f"{condition} detected. Maintenance inspection is recommended."
    }