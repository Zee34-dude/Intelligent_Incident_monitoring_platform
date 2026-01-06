import asyncio
from datetime import datetime, timezone
from sqlalchemy.orm import Session 
from .. import models
from app.database import SessionLocal
from app.models import Service
from app.health.checker import check_service
from .utils import calculate_severity

CHECK_INTERVAL=60

async def health_check_loop():
    while True:
        db: Session = SessionLocal()

        try:
            services = db.query(Service).all()

            for service in services:
                result = await check_service(service.url)
                current_status = result["status"]

                print(
                    f"Service {service.id}: "
                    f"current={current_status}, last={service.last_status}"
                )

                # STATUS CHANGE DETECTED
                if service.last_status != current_status:

                    # 🔻 SERVICE WENT DOWN → CREATE NEW INCIDENT
                    if current_status == "DOWN":
                        active_incident = (
                            db.query(models.Incident)
                            .filter(
                                models.Incident.service_id == service.id,
                                models.Incident.status == "OPEN"
                            )
                            .first()
                        )

                        if not active_incident:
                            new_incident = models.Incident(
                                service_id=service.id,
                                title=f"{service.website_name} is DOWN",
                                status="OPEN",
                                severity=calculate_severity(result),
                                organization_id=service.organization_Id,
                                started_at=datetime.now(timezone.utc),
                            )
                            db.add(new_incident)

                    # 🔺 SERVICE RECOVERED → RESOLVE ACTIVE INCIDENT
                    elif current_status == "UP":
                        active_incident = (
                            db.query(models.Incident)
                            .filter(
                                models.Incident.service_id == service.id,
                                models.Incident.status == "OPEN"
                            )
                            .first()
                        )

                        if active_incident:
                            active_incident.status = "RESOLVED"
                            active_incident.resolved_at = datetime.now(timezone.utc)

                # 🔁 ALWAYS UPDATE SERVICE STATE
                service.status = current_status
                service.last_status = current_status
                service.last_checked_at = datetime.now(timezone.utc)
                service.response_time = result.get("response_time")
                service.error_reason = result.get("error")

            db.commit()

        except Exception as e:
            db.rollback()
            print("Health check error:", e)

        finally:
            db.close()

        await asyncio.sleep(CHECK_INTERVAL)
