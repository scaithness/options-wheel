import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys


LOG_PATH = "logs/run.log"  # ✅ matches your actual log file
print(f"📄 Looking for log at: {LOG_PATH}")

def send_email():
    print("📬 Preparing to send email...")

    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender or not recipient or not password:
        print("❌ Missing email credentials.")
        sys.exit(1)

    try:
        with open(LOG_PATH, "r") as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"❌ Log file not found at {LOG_PATH}.")
        log_content = "⚠️ Strategy log file was not found. The strategy may have failed before logging."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "🧠 Options Wheel Strategy Log Summary"

    body = MIMEText(log_content, "plain")
    msg.attach(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_email()