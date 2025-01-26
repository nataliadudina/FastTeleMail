from celery import shared_task
import logging
from src.notifications.services import schedule_messaging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_notification(self, notification_id: int):
    """
    Celery task that delegates processing to the service layer.
    """
    try:
        logger.info(f"Starting task for notification ID {notification_id}")
        schedule_messaging(notification_id)
        logger.info(f"Task completed successfully for notification ID {notification_id}")
    except Exception as exc:
        logger.error(f"Task failed for notification ID {notification_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)
