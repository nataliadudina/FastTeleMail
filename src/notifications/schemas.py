from datetime import datetime
from enum import Enum

from pydantic import BaseModel, model_validator, Field, ConfigDict


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

    @model_validator(mode='before')
    @classmethod
    def validate_recipient(cls, values) -> list[str]:
        recipient = values.get('recipient')
        if isinstance(recipient, str):
            values['recipient'] = [recipient]
        elif isinstance(recipient, list) and all(isinstance(item, str) for item in recipient):
            pass
        else:
            raise ValueError('Recipient must be either a string or a list of strings.')
        return values

    def get_recipient_as_list(self) -> list[str]:
        """
        Returns list of recipients. If `recipient` id a string, converts it into list
        """
        if isinstance(self.recipient, str):
            return [self.recipient]
        return self.recipient


# DeliveryLog Pydentic Schema
class DeliveryLogBase(BaseModel):
    status: Status
    error_message: str | None


class DeliveryLogResponse(DeliveryLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
