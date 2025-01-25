import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import app_settings

engine = create_engine(app_settings.db.uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        logger.info('Database is ready')
        yield db
    finally:
        db.close()

