import pytest
from fastapi.testclient import TestClient

from app import db_models
from app.database import engine
from app.main import app

client = TestClient(app)


@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


test_chef = {
        "full_name": "Kamleshwar",
        "speciality_cuisine": "Italian",
        "city": "London",
        "mobile": "1234567890",
        "email": "k@g.com",
        "id": 1  # Ensure that data types match the model
    }
# Test the create_chef API


def test_create_chef():

    response = client.post("/chefs/", json=test_chef)

    # Debugging information
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Assertions
    assert response.status_code == 200
    assert "full_name" in response.json()
    assert "city" in response.json()
    assert "speciality_cuisine" in response.json()


def test_get_chefs():
    response = client.get("/chefs/")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)


def test_get_chef_by_id():

    response = client.get("/chefs/id?chef_id=1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == 1


def test_get_chef_by_email():

    response = client.get("/chefs/email?chef_mail=k@g.com")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["email"] == "k@g.com"


def test_get_chef_by_city():

    response = client.get("/chefs/city?chef_city=London")
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["city"] == "London"

