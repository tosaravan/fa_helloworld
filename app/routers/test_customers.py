import pytest
from fastapi.testclient import TestClient

from app import models
from app.database import engine
from app.main import app

client = TestClient(app)


@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


test_customer = {
    "full_name": "Kamleshwar",
    "city": "London",
    "mobile": "1234567890",
    "email": "kam@gam.com",
}


def test_create_customer():
    response = client.post("/customers/", json=test_customer)

    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["full_name"] == "Kamleshwar"
    assert response_json["city"] == "London"


def test_get_customers():

    response = client.get("/customers/")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)


def test_get_customers_by_id():

    response = client.get("/customers/1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == 1


def test_get_customers_by_email():

    response = client.get("/customers/email?customers_mail=k%40g.com")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["email"] == "k@g.com"


def test_get_customers_by_city():

    response = client.get("/customers/city?customers_city=Manchester")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["city"] == "Manchester"




