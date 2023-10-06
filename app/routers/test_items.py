import pytest
from fastapi.testclient import TestClient

from app import db_models
from app.database import engine
from app.main import app

client = TestClient(app)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


# def test_read_items():
#     response = client.get("/items/read")
#     assert response.status_code == 200
#     expected_json = {
#         "gun": {"name": "Portal Gun"},
#         "plumbus": {"name": "Plumbus"}
#     }
#     assert response.json() == expected_json


def test_read_items():
    response = client.get("/items/read")
    assert response.status_code == 200
    expected_json = {
        "gun": {"name": "Portal Gun"},
        "plumbus": {"name": "Plumbus"}
    }
    assert response.json() == expected_json



