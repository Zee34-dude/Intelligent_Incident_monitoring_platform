from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from app import models
from ..health.utils import current_downtime


def get_metrics_by_service(
    organization_id: int,
    db: Session
):
    services = (
        db.query(models.Service)
        .filter(models.Service.organization_Id == organization_id)
        .all()
    )

    metrics = []

    for service in services:
        # ---- INCIDENT COUNT ----
        incident_count = (
            db.query(models.Incident)
            .filter(models.Incident.service_id == service.id)
            .count()
        )

        # ---- SEVERITY DISTRIBUTION ----
        severity_rows = (
            db.query(
                models.Incident.severity,
                func.count(models.Incident.id)
            )
            .filter(models.Incident.service_id == service.id)
            .group_by(models.Incident.severity)
            .all()
        )

        severity_distribution = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0,
        }

        for severity, count in severity_rows:
            severity_distribution[severity] = count

        # ---- MTTR (seconds) ----
        mttr_seconds = (
            db.query(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Incident.resolved_at
                        - models.Incident.started_at
                    )
                )
            )
            .filter(
                models.Incident.service_id == service.id,
                models.Incident.status == "RESOLVED",
                models.Incident.resolved_at.isnot(None)
            )
            .scalar()
        ) or 0

        # ---- DOWNTIME ----
        current_downtime_seconds = (
            current_downtime(service,db)
            if service.status == "DOWN"
            else 0
        )

        total_downtime_seconds = (
            db.query(
                func.sum(
                    func.extract(
                        "epoch",
                        models.Incident.resolved_at
                        - models.Incident.started_at
                    )
                )
            )
            
            .filter(
                models.Incident.service_id == service.id,
                models.Incident.status == "RESOLVED",
                models.Incident.resolved_at.isnot(None)
            )
            .scalar()
        ) or 0
        print(total_downtime_seconds)
        service_life_time=(   
            datetime.now(timezone.utc)-service.created_at
        ).total_seconds()
        total_downtime_seconds = float(total_downtime_seconds or 0)
        current_downtime_seconds = float(current_downtime_seconds or 0)
        uptime_percentage = (
           ((service_life_time-(total_downtime_seconds + current_downtime_seconds))/service_life_time)
        )*100
        total_uptime_seconds=(uptime_percentage/100)*service_life_time
        metrics.append({
            "service_id": service.id,
            "uptime_percentage": uptime_percentage,
            "current_downtime_seconds": int(current_downtime_seconds),
            "total_downtime_seconds": int(total_downtime_seconds),
            "total_uptime_seconds":int(total_uptime_seconds),
            "service_life_time":int(service_life_time),
            "mttr_seconds": int(mttr_seconds),
            "incident_count": incident_count,
            "severity_distribution": severity_distribution,
        })

    return metrics
