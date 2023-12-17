# app/routers/event.py

from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from utils.dependencies import get_db
from models.enums import SortOptions, SortOrder
from models.event import EventCreate, Event


router = APIRouter(prefix="/events", tags=["Event"])


@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event.
    """
    try:
        return Event.create_event(db=db, event=event)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/batch", response_model=List[Event])
def create_events(events: List[EventCreate], db: Session = Depends(get_db)):
    try:
        return Event.create_events(db=db, events=events)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

@router.get("/", response_model=List[Event])
def read_events(skip: int = 0, limit: int = 100, location: str = None, venue: str = None,
                sort_by: SortOptions = None, sort_order: SortOrder=None,
                db: Session = Depends(get_db)):
    try:
        events = Event.get_events(db, skip=skip, limit=limit, location=location, venue=venue, sort_by=sort_by, sort_order=sort_order)
        return events
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    try:
        db_event = Event.get_event(db, event_id=event_id)
        if db_event is None:
            raise HTTPException(status_code=404, detail="event not found")
        return db_event
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.put("/batch", response_model=List[Event])
def update_events(event_updates: List[Event], db: Session = Depends(get_db)):
    try:
        return Event.update_events(db, event_updates)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event.update_event(db, event_id, event)
    if db_event is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="event not found")
    return db_event


@router.delete("/batch", response_model=List[Event])
def delete_events(event_ids: List[int], db: Session = Depends(get_db)):
    try:
        return Event.delete_events(db, event_ids)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.delete("/{event_id}", response_model=Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = Event.delete_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="event not found")
    return db_event
