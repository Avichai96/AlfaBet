# app/router/reminder.py

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from utils.dependencies import get_db

from models.event import Event
from models.reminder import EventReminder, EventReminderCreate


router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.get("/", response_model=List[EventReminder])
def get_reminders(db: Session = Depends(get_db)):
    try:
        return EventReminder.get_reminders(db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/signup-for-reminder/", response_model=EventReminder)
def sign_up_for_reminder(reminder: EventReminderCreate, db: Session = Depends(get_db)):
    db_event = Event.get_event(db, event_id=reminder.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Invalid event")
    if db_event.event_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Event already passed")
    try:
        return EventReminder.sign_up_for_reminder(db, reminder)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

@router.post("/unsubscribe/")
def unsubscribe(reminder_id: int, db: Session = Depends(get_db)):
    try:
        db_reminder = EventReminder.unsubscribe_reminder(db, reminder_id)
        if not db_reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        return {"message": "Unsubscribed successfully", "reminder_details": db_reminder}
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))