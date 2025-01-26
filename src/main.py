import uvicorn
from fastapi import FastAPI

from src.config import AppSettings
from src.notifications.router import notify_router

app = FastAPI(**AppSettings().model_dump())


@app.on_event('startup')
async def on_startup():
    """
    Initialize the database when the application starts.
    """
    from src.database import Base, engine
    from src.notifications.models import Notification, DeliveryLog  # noqa
    Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(notify_router, prefix='/api/notify', tags=['Notifications 📧'])


if __name__ == '__main__':
    uvicorn.run("main:app", reload=False)
