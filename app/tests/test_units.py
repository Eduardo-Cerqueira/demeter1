from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_unit():
    response = client.post(
        "/units/",
        json={"unit": "foo"},
    )
    assert response.status_code == 201


def test_fetch_one_unit():
    response = client.get("/units/foo")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == "foo"


def test_delete_unit():
    response = client.delete("/units/foo")
    assert response.status_code == 204
