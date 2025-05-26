"""
Written by Felipe Rey
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import SMTP_USERNAME, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, ATTORNEY_EMAIL
import logging

logger = logging.getLogger(__name__)


async def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
        )
        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")


async def send_lead_confirmation_email(lead_email: str, lead_name: str):
    subject = "Application Received - Thank You"
    body = f"""
Hi {lead_name},

Thank you for submitting your application. We have received your CV/Resume and will review it shortly.

We will contact you soon regarding the next steps.

Best,

"""
    await send_email(lead_email, subject, body)


async def send_attorney_notification_email(lead_email: str, lead_name: str):
    subject = f"New Lead Application: {lead_name}"
    body = f"""
A new lead application has been submitted:

Name: {lead_name}
Email: {lead_email}

Please review the application in the system.

Best,
"""
    await send_email(ATTORNEY_EMAIL, subject, body)