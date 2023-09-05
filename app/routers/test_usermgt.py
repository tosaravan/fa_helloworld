import pytest
from fastapi.testclient import TestClient

from app import models
from app.database import engine
from app.main import app

client = TestClient(app)

user_payload = {"firstname": "foobar", "lastname": "Foo Bar", "email": "The Foo Barters", "mobile": "Foo Bar",
                "password": "Foo Bar"}
cart_payload = {
        "customer_name": "Kamleshwar",
        "items": [
            {
                "product_name": "One Plus 9 Pro",
                "product_cost": 75000,
                "total_units": 1
            },
            {
                "product_name": "Phone Case ",
                "product_cost": 1500,
                "total_units": 2
            }
        ]
    }


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

def test_create_shopping_cart(test_db):
    response = client.post(
        "/usermgt/cart",
        json=cart_payload,
    )
    assert response.status_code == 200
    assert response.json()=={"customer_name": "Kamleshwar",
        "items": [
            {
                "product_name": "One Plus 9 Pro",
                "product_cost": 75000,
                "total_units": 1
            },
            {
                "product_name": "Phone Case ",
                "product_cost": 1500,
                "total_units": 2
            }
        ]


    }


