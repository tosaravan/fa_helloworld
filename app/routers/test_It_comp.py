import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app.main import app

client = TestClient(app)

job_post_payload = {
    "job_reference": "Python Developer", "job_details": "Advanced python - Fast API", "job_salary": 80000,
    "job_category": "PYTHON", "id": 0, "is_active": True
}


@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_create_job_post(test_db):
    response = client.post(
        "/it_comp/",
        json=job_post_payload,
    )
    assert response.status_code == 200
    assert response.json()["job_category"] == "PYTHON"
    response_json = response.json()
    print(response_json)


# def test_create_job_post(test_db):
#     response = client.post(
#         "/it_comp/",
#         json=job_post_payload,
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     print(response_json)  # This line prints the JSON response content
#     assert response_json["job_category"] == "PYTHON"
def test_get_job_posts(test_db):
    response = client.get(
        "/it_comp/",
        json=job_post_payload
    )
    assert response.status_code == 200


def test_get_job_posts(test_db):
    response = client.get("/it_comp/")
    assert response.status_code == 200



