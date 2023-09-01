import pytest
from fastapi.testclient import TestClient

from app import models
from app.database import engine
from app.main import app

client = TestClient(app)

user_payload = {"firstname": "foobar", "lastname": "Foo Bar", "email": "The Foo Barters", "mobile": "Foo Bar",
                "password": "Foo Bar"}


@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    response = client.post(
        "/usermgt/",
        # headers={"X-Token": "coneofsilence"},
        json=user_payload,
    )
    assert response.status_code == 200
    assert response.json() == {"email": "The Foo Barters",
                               "firstname": "foobar",
                               "id": 1,
                               "is_active": True,
                               "lastname": "Foo Bar",
                               "mobile": "Foo Bar"}
