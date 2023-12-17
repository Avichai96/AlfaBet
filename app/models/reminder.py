# app/models/reminder.py

from typing import List
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from . import sql_models as models
from .event import Event
from utils.tasks import send_email
from utils.database import SessionLocal


class EventReminderBase(BaseModel):
    email: str
    event_id: int


class EventReminderCreate(EventReminderBase):
    pass


class EventReminder(EventReminderBase):
    id: int
    unsubscribed: bool
    event: Event  # Include the related event here

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sign_up_for_reminder(db: Session, reminder: EventReminderCreate):
        db_reminder = models.EventReminder(**reminder.model_dump())
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)
        return db_reminder


    @staticmethod
    def get_reminder(db: Session, reminder_id: int):
        return db.query(models.EventReminder).options(joinedload(models.EventReminder.event)).filter(models.EventReminder.id == reminder_id).first()


    @staticmethod
    def get_reminders(db: Session):
        return db.query(models.EventReminder).options(joinedload(models.EventReminder.event)).all()


    @staticmethod
    def unsubscribe_reminder(db: Session, reminder_id: int):
        db_reminder = EventReminder.get_reminder(db, reminder_id)
        db_reminder.unsubscribed = True
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)
        return db_reminder


    @staticmethod
    def get_upcoming_reminders():
        db = SessionLocal()
        now = datetime.utcnow()
        upcoming_reminders = db.query(models.EventReminder).join(models.Events).filter(
                models.EventReminder.unsubscribed == False,
                models.Events.event_date > now,
                models.Events.event_date <= now + timedelta(minutes=30)
            ).all()
        return upcoming_reminders

    
    @staticmethod
    def send_reminders():
        upcoming_reminders: List[EventReminder] = EventReminder.get_upcoming_reminders()
        for reminder in upcoming_reminders:
            send_email(reminder.email, reminder.event)