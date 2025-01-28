import logging

import requests
from sqlalchemy.orm import Session

from src.celery_app import celery_app
from src.database import get_db
from src.notifications.db import log_delivery
from src.notifications.email_sender import send_email
from src.notifications.models import Notification, Status
from src.notifications.services import send_telegram
from src.notifications.utils import validate_recipients

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def send_notification(self, notification_id: int):
    """
    Celery task that processes a notification by validating recipients,
    sending messages via email or Telegram, and logging the delivery status.
    """
    try:
        db: Session = next(get_db())
        notification = db.query(Notification).get(notification_id)

        recipients = notification.recipient
        subject = notification.subject
        message = notification.message

        valid_emails, valid_telegram_ids, invalid_recipients = validate_recipients(recipients)

        # If no valid recipients, log and stop
        if not valid_emails and not valid_telegram_ids:
            log_delivery(
                notification_id=notification_id,
                status=Status.FAILED,
                error_message=f"No valid recipients. Invalid count: {len(invalid_recipients)}",
            )
            return

        # Send messages if valid recipients found
        if valid_emails:
            send_email(subject=subject, message=message, recipient_list=valid_emails)
        if valid_telegram_ids:
            for tg_id in valid_telegram_ids:
                send_telegram(message=message, chat_id=tg_id)

        # Successful delivery log
        log_delivery(
            notification_id=notification_id,
            status=Status.SENT,
            error_message=f"Valid: {len(valid_emails) + len(valid_telegram_ids)}, Invalid: {len(invalid_recipients)}",
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in task for Notification ID {notification_id}: {str(e)}")
        log_delivery(
            notification_id=notification_id,
            status=Status.FAILED,
            error_message=f"RequestException: {str(e)}",
        )
        raise self.retry(exc=e, countdown=60, max_retries=3)
