from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, Enum as AlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Enum for delay
class Delay(PyEnum):
    INSTANT = 0
    ONE_HOUR = 1
    ONE_DAY = 2


# Enum for status
class Status(PyEnum):
    SENT = 'sent'
    FAILED = 'failed'

    def __str__(self):
        return self.value.capitalize()


# Notification ORM model
class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), default='No Subject')
    message = Column(Text(1024))
    recipient = Column(JSON)
    delay = Column(Integer, default=Delay.INSTANT.value)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship('DeliveryLog', back_populates='notification')

    def __repr__(self):
        return f'Notification to {self.recipient}.'


# DeliveryLog ORM model
class DeliveryLog(Base):
    __tablename__ = 'delivery_logs'

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey('notifications.id'))
    status = Column(AlEnum(Status), default=Status.SENT)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text, nullable=True)

    notification = relationship("Notification", back_populates="logs")

    def __repr__(self):
        return f"Log for Notification {self.notification_id} - {self.status}"
