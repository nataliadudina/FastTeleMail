import uvicorn
from fastapi import FastAPI

from src.config import AppSettings
from src.notifications.router import notify_router

app = FastAPI(**AppSettings().model_dump())

# Register routers
app.include_router(notify_router, prefix='/api/notify', tags=['Notifications 📧'])

if __name__ == '__main__':
    uvicorn.run("main:app", reload=False)
