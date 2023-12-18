# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.sql_models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a fixture for the test client
@pytest.fixture(scope="session")
def test_client():
    with TestClient(app=app) as client:
        yield client

# Create a fixture for the test database session
@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
