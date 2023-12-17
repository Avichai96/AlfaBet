# app/models/sql_models.py

import datetime
from utils.database import engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


Base = declarative_base()


class EventReminder(Base):
    __tablename__ = "event_reminders"

    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'))
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    unsubscribed = Column(Boolean, default=False, nullable=True)

    event = relationship("Events", back_populates="reminders")


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255))
    location = Column(String(255))
    venue = Column(String(255))
    event_date = Column(DateTime, default=datetime.datetime.utcnow)
    popularity = Column(Integer)

    reminders = relationship("EventReminder", back_populates="event")


Base.metadata.create_all(bind=engine)