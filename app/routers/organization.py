from fastapi import APIRouter, Depends, HTTPException,status

from app import models
from app.auth.oaut2 import get_current_user
from app.database import get_db
from .. import schemas
from sqlalchemy.orm import Session
from ..controller import organization_controller


router=APIRouter(
    prefix='/organization',
    tags=['Organization'],
    dependencies=[Depends(get_current_user)] 
)
emailblocklist=[
"gmail.com",

" yahoo.com",

 "outlook.com",

 "hotmail.com",

 "icloud.com",

 "protonmail.com",
]

@router.post('',response_model=schemas.OrganizationCreate)
def create_organization(request:schemas.OrganizationCreate,db:Session=Depends(get_db)):
    domain = request.email.split("@")[1].lower()
    if domain in emailblocklist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please use a business email address"
        )  
  
    new_organization=models.Organization(
        name=request.name,
        email=request.email,
        user_id=request.user_id
    )
    db.query(models.User).filter(models.User.id==request.user_id).update({models.User.role:'admin'},synchronize_session=False)
    
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization
@router.post('/{organization_id}/service',response_model=schemas.ServiceCreate)
def create_service(organization_id:int,request:schemas.ServiceCreate,db:Session=Depends(get_db)):
   return organization_controller.create_service(organization_id,request,db)
@router.patch('/service/{id}',response_model=schemas.ServiceCreate)
def update_service(id:int,request:schemas.ServiceCreate,db:Session=Depends(get_db)):
    return organization_controller.update_service(id,request,db)