import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

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


def test_hello_endpoint():
        name = "Kamleshwar"
        age = '27'
        response = client.get(f"/hello/{name}/{age}")
        assert response.status_code == 200
        expected_json = {"name": name, "age": age}
        assert response.json() == expected_json


def test_create_user_endpoint(test_db):
    user_payload = {
        "firstname": "Kamleshwar",
        "lastname": "MP",
        "email": "MPK@g.com",
        "mobile": "1234567890",
        "password": "qwerty"
    }
    response = client.post("/usermgt/", json=user_payload)
    assert response.status_code == 200

    expected_json = {
        "email": user_payload["email"],
        "firstname": user_payload["firstname"],
        "lastname": user_payload["lastname"],
        "mobile": user_payload["mobile"],
        "id": 1,
        "is_active": True,
    }
    assert response.json() == expected_json
    j_res = response.json()
    print(j_res)




def create_test_user(db: Session, firstname: str, lastname: str, email: str, mobile: str):
    user = models.User(firstname=firstname, lastname=lastname, email=email, mobile=mobile)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
