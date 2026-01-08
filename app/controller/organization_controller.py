from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..import schemas
from app import models 


def create_service(
    organization_id: int,
    request: schemas.ServiceCreate,
    db:Session,

):
  
    print('request',request)
    new_service = models.Service(
        website_name=request.website_name,
        url=request.url,
        status=request.status,
        organization_Id=organization_id
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    
    new_incident=models.Incident(
        service_id=new_service.id,
        title=f"{new_service.website_name} is UP",
        status="RESOLVED",
        resolved_at=datetime.now(timezone.utc),
        severity='LOW',
        organization_id=new_service.organization_Id,
    )
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    
    return new_service

def update_service(
    id:int,
    request: schemas.ServiceCreate,
    db:Session,
):
   service= db.query(models.Service).filter(models.Service.id==id).first()
   if not service:
        raise HTTPException(status_code=404, detail="Service not found") 
   service.url = request.url
   db.commit()
   db.refresh(service)
   return service