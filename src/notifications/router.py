import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.notifications.models import Notification
from src.notifications.schemas import NotificationSchema
from src.notifications.tasks import send_notification
from src.notifications.utils import calculate_eta

logger = logging.getLogger(__name__)

notify_router = APIRouter()


@notify_router.post("/",
                    summary='Send notifications via email or telegram')
async def notify(notification_data: NotificationSchema, db: Session = Depends(get_db)) -> dict[str, bool | str]:
    """
    Create a notification in the database and schedule its sending using Celery task.
    """
    try:
        # Create notification
        notification = Notification(
            subject=notification_data.subject,
            message=notification_data.message,
            recipient=notification_data.recipient,
            delay=notification_data.delay,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        logger.info(f"Notification created successfully: ID={notification.id}")

        # Calculate ETA (Estimated Time of Arrival)
        eta = calculate_eta(notification.delay)

        # Schedule Celery task
        try:
            send_notification.apply_async(args=[notification.id], eta=eta)
        except Exception as e:
            logger.error(f"Failed to schedule Celery task: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to schedule task: {str(e)}")

        return {'success': True, 'message': "Notification scheduled"}

    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create notification: {str(e)}")
