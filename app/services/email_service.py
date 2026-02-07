import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")



def send_email(to_email: str, subject: str, body: str):
    print('to_email', to_email)
    print(SMTP_USER, SMTP_PASSWORD)
    """Send an email using SMTP_SSL"""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(body)
    
    
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


def send_incident_alert(incident, organization):
    print(organization.email)
    """Send alert when a service goes DOWN"""
    subject = f"🚨 ALERT: {incident.title}"
    body = f"""
Incident Details:
-----------------
Title: {incident.title}
Description: {incident.description}
Status: {incident.status}
Severity: {incident.severity}
Organization: {organization.name}

Please investigate immediately.
    """
    send_email(organization.email, subject, body)


def send_incident_resolved(incident, organization):
    """Send notification when incident is resolved"""
    subject = f"✅ RESOLVED: {incident.title}"
    body = f"""
Incident Resolved:
------------------
Title: {incident.title}
Description: {incident.description}
Status: {incident.status}
Severity: {incident.severity}
Organization: {organization.name}

The service is back online.
    """
    send_email(organization.email, subject, body)
 