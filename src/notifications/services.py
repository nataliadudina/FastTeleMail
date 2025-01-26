import logging

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.config import app_settings
from src.notifications.models import DeliveryLog, Notification, Status
from .email_sender import send_email
from .utils import is_valid_email, is_valid_telegram_id
from ..database import get_db

logger = logging.getLogger(__name__)


def schedule_messaging(notification_id: int) -> None:
    """ Schedules messaging for a given notification."""
    try:
        db: Session = next(get_db())
        notification = db.query(Notification).get(notification_id)

        recipients = notification.recipient
        subject = notification.subject
        message = notification.message

        valid_emails = [r for r in recipients if is_valid_email(r)]
        valid_telegram_ids = [r for r in recipients if is_valid_telegram_id(r)]
        invalid_recipients = [r for r in recipients if r not in valid_emails + valid_telegram_ids]

        if not valid_emails and not valid_telegram_ids:
            log_delivery(
                notification_id=notification_id,
                status=Status.FAILED,
                error_message=f"No valid recipients. Invalid recipients count: {len(invalid_recipients)}",
            )
            return

        if valid_emails:
            send_email(subject=subject, message=message, recipient_list=valid_emails)
        if valid_telegram_ids:
            for tg_id in valid_telegram_ids:
                send_telegram(message=message, chat_id=tg_id)

        log_delivery(
            notification_id=notification_id,
            status=Status.SENT,
            error_message=f"Valid recipients: {len(valid_emails) + len(valid_telegram_ids)}, "
                          f"Invalid recipients: {len(invalid_recipients)}",
        )

    except Exception as e:
        logger.error(f"Error in schedule_messaging: {str(e)}")
        log_delivery(
            notification_id=notification_id,
            status=Status.FAILED,
            error_message=f"Error: {str(e)}",
        )
        raise HTTPException(status_code=500, detail="Internal server error")


def send_telegram(message: str, chat_id: str) -> None:
    """ Sends a message via Telegram API."""
    url = app_settings.telegram.TELEGRAM_URL
    token = app_settings.telegram.TELEGRAM_API_TOKEN
    try:
        response = requests.post(url=f'{url}{token}/sendMessage?chat_id={chat_id}&text={message}')
        response.raise_for_status()
        logger.info(f"Telegram message sent to chat_id {chat_id}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message to chat_id {chat_id}: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: Unable to send Telegram message")


def log_delivery(notification_id: int, status: Status, error_message: str = None) -> None:
    """Log the delivery status to the DeliveryLog table."""
    try:
        db: Session = next(get_db())
        log_entry = DeliveryLog(
            notification_id=notification_id,
            status=status,
            error_message=error_message,
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Error while writing to log: {str(e)}")
