# communications/utils.py
import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY

def send_email(to, CC, subject, content):
    if not settings.RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY is not set in settings")
    try:
        r = resend.Emails.send({
            "from": "your-verified-email@example.com",  # Replace with your verified sender email
            "to": to,
            #remember they are many shops, so we need to use the shop's email
            "cc": "CC",
            "subject": subject,
            "html": content,
        })
        return r
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise