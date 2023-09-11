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


def test_hello_endpoint():
    name = "Kamleshwar"
    age = '27'
    response = client.get(f"/hello/{name}/{age}")
    assert response.status_code == 200
    expected_json = {"name": name, "age": age}
    assert response.json() == expected_json