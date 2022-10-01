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


def test_hello():
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    result = response.json()
    assert result == {"msg": "Hello World"}
    logging.info(result)
