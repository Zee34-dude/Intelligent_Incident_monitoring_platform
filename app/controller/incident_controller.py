from datetime import datetime, timezone
from http.client import HTTPException
from sqlalchemy.orm import Session
from app import models
from ..schemas import Incident

INCIDENT_TRANSITIONS = {
    "OPEN": {"INVESTIGATING"},
    "INVESTIGATING": {"RESOLVED"},
    "RESOLVED": set(),
}


def update_incident_status(
    request:Incident,
    incident_id:int,
    db:Session
):
   incident=db.query(models.Incident).filter(models.Incident.id==incident_id).first()
   if incident.status != "OPEN":
    raise HTTPException(400, "Only OPEN incidents can be investigated")

   incident.status = "INVESTIGATING"
   incident.investigating_at = datetime.now(timezone.utc)
   incident.investigated_by = request.user.id
   incident.investigation_note = request.note
    