import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import credentials # email username and password

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
