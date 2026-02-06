from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from datetime import timezone
from app.database import get_db
from typing import Optional
from ..controller import incident_controller
from ..schemas import Incident
from .. import models

router=APIRouter(
 prefix='/incidents',
 tags=['Incident']
)

@router.get("/organization/{organization_id}")
def list_incidents(
    organization_id:int,
    db:Session=Depends(get_db),
    status:Optional[str]=Query(None),
    limit:int=Query(10,ge=1,le=100),
    skip:int=Query(0)
):
    query=db.query(models.Incident).filter(models.Incident.organization_id==organization_id)
    #Add Optional status filter
    if status:
        query=query.filter(models.Incident.status==status)
    
    #NOW apply pagination
    incidents=query.offset(skip).limit(limit).all()
    return incidents

@router.get('/{id}')
def get_incident(id: int, db: Session = Depends(get_db)):
    incident=db.query(models.Incident).filter(models.Incident.id==id).first()
    if not incident:
        raise HTTPException(404,"Incident not found")
    return incident 

@router.post('/{id}/acknowledge')
def acknowledge_incident(
    id:int,
    user_id:int,
    db:Session=Depends(get_db)
):
  incident=db.query(models.Incident).filter(models.Incident.id==id).first()
  if not incident:
    raise HTTPException(404,"Incident not found")
  if incident.status=="ACKNOWLEDGED":
    raise HTTPException(400,"Incident already acknowledged")  
  incident.status="ACKNOWLEDGED"
  incident.acknowledged_at=datetime.now(timezone.utc)
  incident.investigated_by=user_id
  db.commit()
  return incident
@router.post('/{id}/resolve')
def resolve_incident(
    id:int,
    user_id:int,
    note:Optional[str]=None,
    db:Session=Depends(get_db)
):
    incident=db.query(models.Incident).filter(models.Incident.id==id).first()
    if not incident:
        raise HTTPException(404,"Incident not found")
    if incident.status=="RESOLVED":
        raise HTTPException(400,"Incident already resolved")
    incident.status="RESOLVED"
    incident.investigation_note=note
    incident.resolved_at=datetime.now(timezone.utc)
    incident.investigated_by=user_id
    db.commit()
    return incident

@router.patch('/{incident_id}/investigate',response_model=Incident)
def update_incident_status(request:Incident,incident_id,db:Session=Depends(get_db)):
    incident_controller.update_incident_status(request,incident_id,db)