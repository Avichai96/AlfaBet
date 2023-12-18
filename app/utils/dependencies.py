# app/utils/dependencies.py

from utils.database import SessionLocal


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()