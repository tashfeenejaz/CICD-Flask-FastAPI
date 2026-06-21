from fastapi.testclient import TestClient
from main import app, tasks

client = TestClient(app)


def setup_function():
    """Clear tasks before each test to ensure isolation."""
    tasks.clear()


# def test_health():
#     """GET /health should return 200 and status ok."""
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 999  # wrong status code

def test_create_task():
    """POST /tasks with valid payload returns 201 and the created task."""
    payload = {"title": "Write tests", "done": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["done"] is False


def test_get_tasks_grows():
    """GET /tasks returns a list that grows after a task is created."""
    # Initially empty
    response = client.get("/tasks")
    assert response.status_code == 200
    initial_count = len(response.json())

    # Create a task
    client.post("/tasks", json={"title": "Buy groceries"})

    # List should grow by 1
    response = client.get("/tasks")
    assert response.status_code == 200
    updated = response.json()
    assert len(updated) == initial_count + 1
    assert any(t["title"] == "Buy groceries" for t in updated)


def test_create_task_empty_title_fails():
    """POST /tasks with empty title should return 400 Bad Request."""
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
    assert "detail" in response.json()
