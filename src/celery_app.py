from celery import Celery

app = Celery(
    "FastTeleMail",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.autodiscover_tasks(["src.notifications.tasks"])

# Celery settings
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    celery_task_ignore_result=False,
    broker_connection_retry_on_startup=True
)
