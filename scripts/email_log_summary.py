import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

LOG_PATH = "logs/strategy.log"  # Adjust if your log path differs

def send_email():
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_APP_PASSWORD")

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "🧠 Strategy Log Summary"

    body = MIMEText(log_content, "plain")
    msg.attach(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

if __name__ == "__main__":
    send_email()