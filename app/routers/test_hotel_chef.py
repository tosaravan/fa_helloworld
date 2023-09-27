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



