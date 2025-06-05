import smtplib
import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import requests

# Email Configuration
FROM_EMAIL = "<EMAIL>"
PASSWORD = "<APP PASSWORD>"
TO_EMAIL = "<EMAIL>"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Telegram Configuration
TELEGRAM_TOKEN = '<TELEGRAM BOT_FATHER TOKEN>'
GROUP_CHAT_ID = '<TELEGRAM GROUP ID>'

# Logger Configuration
logger = logging.getLogger("InternetMonitor")
logger.setLevel(logging.INFO)

# Rotating log handler, rotates every month
handler = TimedRotatingFileHandler("internet_monitor.log", when="midnight", interval=1)
handler.suffix = "%Y-%m"
handler.extMatch = r"^\d{4}-\d{2}$"
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def send_email():
    """Sends an email notification."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        
        # Encode message in UTF-8
        subject = "Internet Restored"
        body = "The internet connection has been recovered."
        message = f"Subject: {subject}\n\n{body}".encode("utf-8")

        server.sendmail(FROM_EMAIL, TO_EMAIL, message)
        server.quit()
        logger.info("E-mail delivered with success")
    except Exception as e:
        logger.error(f"E-mail deliver failure: {e}")

def send_telegram_message(token, chat_id, message):
    """Sends a message via Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.info("Telegram message sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Telegram message deliver failure: {e}")

def check_internet():
    """Checks if the internet is reachable."""
    hostname = "<IP>" # IMPORTANT: Replace <IP> with a reliable IP to ping, e.g., '8.8.8.8'
    response = os.system(f"ping -c 4 {hostname}")
    return response == 0

was_offline = False

while True:
    if check_internet():
        if was_offline:
            logger.info("Internet connection recovered.") # Log recovery
            send_email()
            send_telegram_message(TELEGRAM_TOKEN, GROUP_CHAT_ID, "The internet connection has been recovered.")
            was_offline = False
        # else: # Optional: Log if internet is still online
            # logger.info("Internet connection is online.")
    else:
        if not was_offline: # Log loss only once
            logger.warning("Internet connection lost.") # Changed to warning for better visibility
            # send_telegram_message(TELEGRAM_TOKEN, GROUP_CHAT_ID, "Alert: Internet connection lost.") # Optional: Notify on loss
        was_offline = True
    time.sleep(60) # Check every 60 seconds
