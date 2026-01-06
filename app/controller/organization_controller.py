from fastapi import Depends, HTTPException
from app.auth.dependencies import require_org_role
from app.database import get_db
from sqlalchemy.orm import Session
from ..models import Service
from ..import schemas
from app import models 


def create_service(
    organization_id: int,
    request: schemas.ServiceCreate,
    db:Session,

):
  
    print('request',request)
    new_service = Service(
        website_name=request.website_name,
        url=request.url,
        status=request.status,
        organization_Id=organization_id
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

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