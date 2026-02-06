import asyncio
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal
from app.models import Service, Organization
from app.health.checker import check_service
from app.health.utils import calculate_severity
from app.services.email_service import send_incident_alert, send_incident_resolved

CHECK_INTERVAL = 60


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
                if service.last_status and service.last_status != current_status:

                    # Get organization for email
                    organization = db.query(Organization).filter(
                        Organization.id == service.organization_Id
                    ).first()

                    # 🔻 SERVICE WENT DOWN → CREATE NEW INCIDENT
                    if current_status == "DOWN":
                        new_incident = models.Incident(
                            service_id=service.id,
                            title=f"{service.website_name} is DOWN",
                            status="OPEN",
                            severity=calculate_severity(result),
                            organization_id=service.organization_Id,
                            description=result.get("error"),
                        )
                        db.add(new_incident)
                        db.flush()  # Get the incident ID before commit

                        # 📧 SEND ALERT EMAIL
                        try:
                            await asyncio.to_thread(send_incident_alert, new_incident, organization)
                            print(f"Alert email sent for {service.website_name}")
                        except Exception as email_error:
                            print(f"Failed to send alert email: {email_error}")

                    # 🔺 SERVICE RECOVERED → RESOLVE ACTIVE INCIDENT
                    elif current_status == "UP":
                        latest_incident = (
                            db.query(models.Incident)
                            .filter(models.Incident.service_id == service.id)
                            .order_by(models.Incident.created_at.desc())
                            .first()
                        )
                        new_incident = models.Incident(
                            service_id=service.id,
                            title=f"{service.website_name} is UP",
                            status="RESOLVED",
                            severity=calculate_severity(result),
                            organization_id=service.organization_Id,
                            started_at=latest_incident.created_at if latest_incident else None,
                            resolved_at=datetime.now(timezone.utc)
                        )
                        db.add(new_incident)

                        # 📧 SEND RESOLVED EMAIL
                        try:
                            await asyncio.to_thread(send_incident_resolved, new_incident, organization)
                            print(f"Resolved email sent for {service.website_name}")
                        except Exception as email_error:
                            print(f"Failed to send resolved email: {email_error}")

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

