from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..health.utils import current_downtime 

from app import models

def get_metrics_by_organization(organization_id:int,db:Session):
    total_incidents= db.query(models.Incident).filter(
        organization_id==models.Incident.organization_id,
    ).count()
    
    open_incidents= (
        db.query(models.Incident).filter(
            organization_id==models.Incident.organization_id,
            models.Incident.status=='OPEN'
        )
        .count()
        )
    resolved_incidents=total_incidents-open_incidents
    
   # ---- MTTR (Mean Time To Resolve) ----
    mttt_seconds=(
       db.query(
           func.avg(
              func.extract(
                  "epoch",
                    models.Incident.resolved_at-models.Incident.created_at
              ) 
           )
       )
       .filter(
           models.Incident.organization_id==organization_id,
           models.Incident.status=='RESOLVED',
           models.Incident.resolved_at.isnot(None)
       )
       .scalar()
   )
    mttr_minutes=round(mttt_seconds/60,2) if mttr_minutes else None 
    
    services=(
        db.query(models.Service).filter(
           models.Service.organization_Id==organization_id 
        )
    )
    
    service_metrics=[]
    for service in services:
        service_total=(
            db.query(models.Incident)
            .filter(models.Incident.service_id==service.id)
            .count()
        )
        service_open=(
            db.query(models.Incident)
            .filter(
                models.Incident.service_id == service.id,
                models.Incident.status == "OPEN"
            )
            .count()
        )
        last_incident=(
            db.query(models.Incident.created_at)
            .filter(models.Incident.service_id==service.id)
            .order_by(models.Incident.created_at.desc())
            .first()
        )
        service_metrics.append({
            "service_id": service.id,
            "service_name": service.website_name,
            "total_incidents": service_total,
            "open_incidents": service_open,
            "last_incident_at": last_incident[0] if last_incident else None
        })
        return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
        "mean_time_to_resolve_minutes": mttr_minutes,
        "services": service_metrics
     }
        
def get_metrics_by_service(organization_id:int,db:Session):
    total_incidents= db.query(models.Incident).filter(
        organization_id==models.Incident.organization_id,
    ).count()
    
    open_incidents= (
        db.query(models.Incident).filter(
            organization_id==models.Incident.organization_id,
            models.Incident.status=='OPEN'
        )
        .count()
        )
    resolved_incidents=total_incidents-open_incidents
    
   # ---- MTTR (Mean Time To Resolve) ----
    mttt_seconds=(
       db.query(
           func.avg(
              func.extract(
                  "epoch",
                    models.Incident.resolved_at-models.Incident.created_at
              ) 
           )
       )
       .filter(
           models.Incident.organization_id==organization_id,
           models.Incident.status=='RESOLVED',
           models.Incident.resolved_at.isnot(None)
       )
       .scalar()
   )
    mttr_minutes=round(mttt_seconds/60,2) if mttr_minutes else None 
    
    services=(
        db.query(models.Service).filter(
           models.Service.organization_Id==organization_id 
        )
    )
    
    service_metrics=[]
    for service in services:
        service_total=(
            db.query(models.Incident)
            .filter(models.Incident.service_id==service.id)
            .count()
        )
        service_open=(
            db.query(models.Incident)
            .filter(
                models.Incident.service_id == service.id,
                models.Incident.status == "OPEN"
            )
            .count()
        )
        last_incident=(
            db.query(models.Incident.created_at)
            .filter(models.Incident.service_id==service.id)
            .order_by(models.Incident.created_at.desc())
            .first()
        )
        service_metrics.append({
            "service_id": service.id,
            "service_name": service.website_name,
            "total_incidents": service_total,
            "open_incidents": service_open,
            "last_incident_at": last_incident[0] if last_incident else None
        })
        return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
        "mean_time_to_resolve_minutes": mttr_minutes,
        "services": service_metrics
     }
        
      