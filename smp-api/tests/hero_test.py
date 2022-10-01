import logging
import os
import sys

from fastapi.testclient import TestClient

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT_DIR, "app"))
# this is to include backend dir in sys.path so that we can import from db,main.py

from main import app

# from models import Hero, HeroCreate, HeroRead, HeroUpdate
logging.basicConfig(level=logging.INFO)

client = TestClient(app)


def test_read_items():
    response = client.get(
        "/heroes", headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result != []
    logging.info(result)


def test_read_item():
    response = client.get(
        "/hero/1", headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result != {}
    logging.info(result)


def test_create_item():
    response = client.post(
        "/heroes/",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"name": "ABC", "secret_name": "foo bar", "age": 35},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["secret_name"] is not None
    logging.info(result)


def test_update_item():
    response = client.get(
        "/heroes/last", headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200
    origin_result = response.json()
    assert "id" in origin_result
    item_id = origin_result["id"]

    origin_result["name"] += " Super"
    origin_result["age"] = None
    origin_result["team_id"] = 1

    response = client.patch(
        f"/heroes/{item_id}",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={
            "name": origin_result["name"],
            "age": origin_result["age"],
            "team_id": origin_result["team_id"],
        },
    )
    assert response.status_code == 200
    updated_result = response.json()
    assert updated_result == origin_result
    logging.info(updated_result)


def test_delete_item():
    response = client.get(
        "/heroes/last", headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200
    result = response.json()
    assert "id" in result

    item_id = result["id"]
    response = client.delete(
        f"/heroes/{item_id}",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    logging.info(response.json())

    response = client.get(
        f"/hero/{item_id}",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    assert response.status_code == 404
