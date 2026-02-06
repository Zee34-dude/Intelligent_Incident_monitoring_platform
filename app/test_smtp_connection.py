import socket

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # STARTTLS

try:
    with socket.create_connection((SMTP_HOST, SMTP_PORT), timeout=10) as s:
        print(f"✅ Can connect to {SMTP_HOST}:{SMTP_PORT}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
