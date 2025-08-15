import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

LOG_PATH = "logs/run.log"  # ✅ Matches your actual log file

def send_email():
    print(f"📄 Looking for log at: {LOG_PATH}")

    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender or not recipient or not password:
        print("❌ Missing email credentials.")
        sys.exit(1)

    if not os.path.exists(LOG_PATH):
        print("❌ Log file not found.")
        log_content = "⚠️ Strategy log file was not found. The strategy may have failed before logging."
    else:
        with open(LOG_PATH, "r") as f:
            log_content = f.read()

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