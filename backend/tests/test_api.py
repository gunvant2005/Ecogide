import pytest

from app.main import app
from app.services import storage


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "ecoguide.db"
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage, "DB_FILE", db_file)
    monkeypatch.setattr(storage, "PROFILE_FILE", tmp_path / "profile.json")
    monkeypatch.setattr(storage, "ACTIVITIES_FILE", tmp_path / "activities.json")
    storage.init_db()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_profile_crud(client):
    res = client.get("/api/profile")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Alex"

    res = client.put("/api/profile", json={
        "name": "Jordan",
        "household_size": 2,
        "primary_transport": "train",
        "diet_type": "vegetarian",
        "weekly_goal_kg": 70,
        "home_type": "house",
    })
    assert res.status_code == 200
    assert res.get_json()["name"] == "Jordan"


def test_create_activity(client):
    res = client.post("/api/activities", json={
        "category": "transport",
        "sub_type": "bus",
        "quantity": 5,
        "unit": "km",
        "date": "2025-06-20",
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["emissions_kg"] == 0.5
    assert "id" in data


def test_assistant_chat(client):
    client.post("/api/demo/seed")
    res = client.post("/api/assistant/chat", json={"message": "How am I doing?"})
    assert res.status_code == 200
    body = res.get_json()
    assert "reply" in body
    assert body["intent"] == "footprint_status"


def test_footprint_summary(client):
    client.post("/api/demo/seed")
    res = client.get("/api/footprint/summary")
    assert res.status_code == 200
    assert res.get_json()["total_kg"] > 0
