import asyncio
import logging
from smtplib import SMTPException
from typing import List

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors

from src.config import app_settings

logger = logging.getLogger(__name__)

email_settings = app_settings.email

# Set up SMTP connection configuration
conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.EMAIL_USER,
    MAIL_PASSWORD=email_settings.EMAIL_PASSWORD,
    MAIL_FROM=email_settings.EMAIL_USER,
    MAIL_PORT=email_settings.EMAIL_PORT,
    MAIL_SERVER=email_settings.EMAIL_HOST,
    MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)


def send_email(subject: str, message: str, recipient_list: List[str]) -> None:
    """
    Send email notification.
    """
    try:
        email_message = MessageSchema(
            subject=subject,
            recipients=recipient_list,
            body=message,
            subtype="plain"
        )

        fm = FastMail(conf)
        asyncio.run(fm.send_message(email_message))
        logger.info("Email sent successfully")

    except ConnectionErrors as conn_err:
        logger.error(f"Connection error when sending email: {str(conn_err)}")
    except SMTPException as smtp_err:
        logger.error(f"SMTP error when sending email: {str(smtp_err)}")
