from datetime import datetime, timezone

def calculate_severity(service, result):
    status = result.get("status")
    status_code = result.get("status_code")
    response_time = result.get("response_time", 0)

    # Service is DOWN → HIGH or CRITICAL based on status code
    if status == "DOWN":
        if status_code and status_code >= 500:
            return "CRITICAL"
        return "HIGH"

    # Service is UP but slow
    if status == "UP" and response_time > 2000:
        return "MEDIUM"

    return "LOW"

def current_downtime(incident):
    end_time = incident.resolved_at or datetime.now(timezone.utc)
    return (end_time - incident.created_at).total_seconds()
