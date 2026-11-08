from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from src.database import Base, get_db
from src.models import Task
from src.task_list_api import app
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_task(client):
   response = client.post(url="/tasks",
                              json= {
                                  "task": "go to latina night"
                                })
   return response.json()

load_dotenv()
test_db_url = os.getenv("TEST_DATABASE_URL")
if test_db_url is None:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

test_engine = create_engine(test_db_url, echo=True)
TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def clean_test_db():
    db = TestSessionLocal()
    try:
        db.query(Task).delete()
        db.commit()

        yield db
        
        db.query(Task).delete()
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db