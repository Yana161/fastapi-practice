from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[app.main.get_db] = override_get_db

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI"}


def test_create_item():
    response = client.post(
        "/items/", json={"title": "Test Item", "description": "Test desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
