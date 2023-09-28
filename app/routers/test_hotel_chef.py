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


# Test the create_chef API

def test_create_chef():
    # Correct the field names and data types in your test data
    test_chef = {
        "full_name": "Kamleshwar",
        "speciality_cuisine": "Italian",
        "city": "London",
        "mobile": "1234567890",
        "email": "k@g.com",
        "id": 1  # Ensure that data types match the model
    }

    response = client.post("/chefs/", json=test_chef)

    # Debugging information
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Assertions
    assert response.status_code == 200
    assert "full_name" in response.json()
    assert "city" in response.json()
    assert "speciality_cuisine" in response.json()

