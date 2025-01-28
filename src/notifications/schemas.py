from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


# Enum for delay
class Delay(Enum):
    INSTANT = 0
    ONE_HOUR = 1
    ONE_DAY = 2


# Enum for status
class Status(Enum):
    SENT = 'sent'
    FAILED = 'failed'

    def __str__(self):
        return self.value.capitalize()


# Notification Pydentic Schema
class NotificationSchema(BaseModel):
    subject: str = Field(max_length=50, default='No Subject')
    message: str = Field(max_length=1000)
    recipient: list[str] | str
    delay: int = Delay.INSTANT.value

    model_config = ConfigDict(extra='forbid')


# DeliveryLog Pydentic Schema
class DeliveryLogBase(BaseModel):
    status: Status
    error_message: str | None


class DeliveryLogResponse(DeliveryLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
