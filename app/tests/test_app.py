import pytest

import app as taskflow


@pytest.fixture
def client():
    # Reset in-memory data so every test starts clean.
    taskflow.tasks.clear()
    taskflow.next_id = 1
    taskflow.app.config["TESTING"] = True
    with taskflow.app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_version_defaults_to_dev(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert client.get("/version").get_json()["version"] == "dev"


def test_version_reads_env(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    assert client.get("/version").get_json()["version"] == "1.2.3"


def test_create_and_list_tasks(client):
    resp = client.post("/tasks", json={"title": "Learn Terraform"})
    assert resp.status_code == 201
    assert resp.get_json() == {"id": 1, "title": "Learn Terraform", "done": False}
    assert len(client.get("/tasks").get_json()) == 1


def test_create_task_requires_title(client):
    assert client.post("/tasks", json={}).status_code == 400


def test_complete_task(client):
    client.post("/tasks", json={"title": "Write Dockerfile"})
    resp = client.patch("/tasks/1")
    assert resp.status_code == 200
    assert resp.get_json()["done"] is True


def test_delete_task(client):
    client.post("/tasks", json={"title": "Temp"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.delete("/tasks/1").status_code == 404