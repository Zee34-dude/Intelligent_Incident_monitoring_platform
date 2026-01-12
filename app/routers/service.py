from typing import List
from fastapi import APIRouter,Depends
from .. import schemas 
from ..database import get_db
from sqlalchemy.orm import Session
from ..controller import service_controller

router=APIRouter(
    prefix='/services',
    tags=['Services']
)

# @router.post ('',response_model=schemas.IncidentCreate)
# def create_incident(request:schemas.IncidentCreate,db:Session=Depends(get_db)):
#     return service_controller.create_incident(request,db)

@router.get('/{organization_id}/metrics',response_model=List[schemas.ServiceMetrics])
def get_metrics_by_organization(organization_id:int,db:Session=Depends(get_db)):
   return service_controller.get_metrics_by_service(organization_id,db)
    