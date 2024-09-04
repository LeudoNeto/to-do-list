import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models import tasks as models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    models.Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    models.Base.metadata.drop_all(bind=engine)

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Integration Task", "description": "Integration Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Integration Task"
    assert data["description"] == "Integration Description"
    assert data["completed"] is False

def test_get_task(client):
    response = client.post("/tasks/", json={"title": "Integration Task", "description": "Integration Description"})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Integration Task"
    assert data["description"] == "Integration Description"

def test_update_task(client):
    response = client.post("/tasks/", json={"title": "Integration Task", "description": "Integration Description"})
    task_id = response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

def test_partial_update_task(client):
    response = client.post("/tasks/", json={"title": "Integration Task", "description": "Integration Description"})
    task_id = response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True

def test_get_all_tasks(client):
    client.post("/tasks/", json={"title": "Task 1", "description": "Description 1"})
    client.post("/tasks/", json={"title": "Task 2", "description": "Description 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Should have at least 2 tasks

def test_delete_task(client):
    response = client.post("/tasks/", json={"title": "Integration Task", "description": "Integration Description"})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
