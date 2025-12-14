from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app import models

# Тестовая БД
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test_test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


app.dependency_overrides[get_db] = override_get_db
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
    assert "id" in data


def test_read_item():
    # Создаем item
    post_response = client.post(
        "/items/", json={"title": "Test2", "description": "desc2"}
    )
    item_id = post_response.json()["id"]

    # Читаем
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test2"
