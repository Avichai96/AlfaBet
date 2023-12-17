# app/models/event.py

from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from fastapi import HTTPException
from . import sql_models as models
from .enums import SortOrder, SortOptions


class EventBase(BaseModel):
    title: str
    description: str
    venue: str
    location: str
    event_date: datetime
    popularity: int


class EventCreate(EventBase):
    ...


class EventUpdate(EventBase):
    id: int


class Event(EventBase):
    id: int 
    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def get_event(db: Session, event_id: int):
        return db.query(models.Events).filter(models.Events.id == event_id).first()


    @staticmethod
    def get_events(db: Session, skip: int = 0, limit: int = 100, location: str=None, venue: str=None,
                sort_by: Optional[SortOptions]=None, sort_order: SortOrder = SortOrder.asc.value):
        query = db.query(models.Events)

        if location:
            query = query.filter(models.Events.location == location)
        if venue:
            query = query.filter(models.Events.venue == venue)

        # Sorting logic
        order = asc if sort_order == "asc" else desc
        if sort_by:
            match sort_by:
                case SortOptions.date:
                    query = query.order_by(order(models.Events.event_date))
                case SortOptions.popularity:
                    query = query.order_by(order(models.Events.popularity))
                case SortOptions.creation:
                    query = query.order_by(order(models.Events.id))  # Assuming ID represents creation order
                case _:
                    ...

        return query.offset(skip).limit(limit).all()


    @staticmethod
    def create_event(db: Session, event: EventCreate):
        db_event = models.Events(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    

    @staticmethod
    def create_events(db: Session, events: List[EventCreate]):
        db_events = [models.Events(**event.model_dump()) for event in events]
        db.add_all(db_events)
        db.commit()
        for event in db_events:
            db.refresh(event)
        return db_events


    @staticmethod
    def update_event(db: Session, event_id: int, event: EventCreate):
        db_event = Event.get_event(db, event_id)
        if db_event:
            update_data = event.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_event, key, value)
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
        return db_event
    

    @staticmethod
    def update_events(db: Session, event_updates: List[EventUpdate]):
        updated_events = []
        for update in event_updates:
            db_event = db.query(models.Events).filter(models.Events.id == update.id).first()
            if db_event:
                for key, value in update.model_dump(exclude_unset=True).items():
                    setattr(db_event, key, value)
                db.add(db_event)
                updated_events.append(update.id)
        db.commit()
        return [Event.get_event(db, event_id) for event_id in updated_events]


    @staticmethod
    def delete_event(db: Session, event_id: int):
        db_event = Event.get_event(db, event_id)
        if db_event:
            db.delete(db_event)
            db.commit()
        return db_event
    

    @staticmethod
    def delete_events(db: Session, event_ids: List[int]):
        events_to_delete = db.query(models.Events).filter(models.Events.id.in_(event_ids)).all()
        if not events_to_delete:
            raise HTTPException(status_code=404, detail="Events not found")

        deleted_events = [Event.from_orm(event).model_dump() for event in events_to_delete]

        db.query(models.Events).filter(models.Events.id.in_(event_ids)).delete(synchronize_session=False)
        db.commit()

        return deleted_events