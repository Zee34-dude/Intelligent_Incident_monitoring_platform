from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import models

def calculate_severity( result):
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

def current_downtime(service,db:Session):
    lastest_incident=( 
    db.query(models.Incident)
    .filter(
    models.Incident.service_id==service.id)
    .order_by(models.Incident.created_at.desc())
    .first()
  )
    
    if lastest_incident.resolved_at:
        return 0
    else:
        return (datetime.now(timezone.utc)-lastest_incident.created_at).total_seconds()