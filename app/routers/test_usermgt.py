from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

user_payload = {"firstname": "foobar", "lastname": "Foo Bar", "email": "The Foo Barters", "mobile": "Foo Bar", "password": "Foo Bar"}


def test_create_user():
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
