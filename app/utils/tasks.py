import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_address, event):
    # Email server configuration
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'your-email@example.com'
    smtp_password = 'your-password'

    # Email content
    subject = f"Reminder: {event.title}"
    body = f"Don't forget about your upcoming event: {event.title} on {event.event_date}"

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = to_address
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    text = message.as_string()

    # Sending the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_address, text)
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}. Error: {e}")