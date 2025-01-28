import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.notifications.models import Notification, Status, DeliveryLog
from src.notifications.schemas import NotificationSchema
from ..database import SessionLocal

logger = logging.getLogger(__name__)


def create_notification(data: NotificationSchema, db: Session) -> Notification:
    """
    Create a new notification in the database.
    """
    notification = Notification(
        subject=data.subject,
        message=data.message,
        recipient=data.recipient,
        delay=data.delay,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def log_delivery(notification_id: int, status: Status, error_message: str = None) -> None:
    """Log the delivery status to the DeliveryLog table."""
    with SessionLocal() as db:
        try:
            log_entry = DeliveryLog(
                notification_id=notification_id,
                status=status,
                error_message=error_message,
            )
            db.add(log_entry)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error while writing to log: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while writing to log: {type(e).__name__}: {str(e)}")
