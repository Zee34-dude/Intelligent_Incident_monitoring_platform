import smtplib
from email.message import EmailMessage

def send_verification_email(email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = "zionubesie@gmail.com"
    msg["To"] = email
    msg.set_content(f"Your verification code is: {code}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("zionubesie@gmail.com", "vngz hmsz isgc yttj")
        server.send_message(msg)
