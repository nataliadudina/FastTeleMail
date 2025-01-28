import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.notifications.db import create_notification
from src.notifications.schemas import NotificationSchema
from src.notifications.tasks import send_notification
from src.notifications.utils import calculate_eta

logger = logging.getLogger(__name__)

notify_router = APIRouter()


@notify_router.post("/",
                    summary='Send notifications via email or telegram')
def notify(notification_data: NotificationSchema, db: Session = Depends(get_db)) -> dict[str, bool | str]:
    """
    Create a notification in the database and schedule its sending using Celery task.
    """

    # Create a notification
    notification = create_notification(notification_data, db)

    try:
        # Celery task
        send_notification.apply_async(
            args=[notification.id],
            eta=calculate_eta(notification.delay),
        )
        logger.info(f"Task scheduled successfully for Notification ID={notification.id}")

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Failed to connect to task broker: {str(e)}")
        raise HTTPException(status_code=503, detail="Failed to connect to task broker")

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")

    return {"success": True, "message": "Notification scheduled"}
