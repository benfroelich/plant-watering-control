import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import credentials # email username and password

_watering_message_sent_timestamp = 0
def send_nag_message(recipients, subject, body):
    watering_message_interval = 24 # interval in hrs for nag email
    global _watering_message_sent_timestamp
    current_timestamp = time.time()
    if(current_timestamp - _watering_message_interval * 3600 > _watering_message_sent_timestamp):
        print("sending nag email \"{}\"".format(subject))
        _watering_message_sent_timestamp = current_timestamp
        notifier.send_notification(recipients, subject, body) 

def send_notification(recipients, subject, body):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = credentials.username
    message["To"] = recipients
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(credentials.username, credentials.password)
        server.sendmail(credentials.username, recipients, message.as_string())

def main():
    send_notification("benfroelich@gmail.com", "test message", "message contents here")

if __name__ == "__main__":
    main()
