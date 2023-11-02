from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_unit():
    response = client.post(
        "/units/",
        json={"unit": "foo"},
    )
    assert response.status_code == 201

    response = client.post(
        "/units/",
        json={"unit": "bar"},
    )

    assert response.status_code == 201


def test_fetch_all_units():
    response = client.get("/units")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == [["foo"], ["bar"]]


def test_fetch_one_unit():
    response = client.get("/units/foo")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == "foo"


def test_put_unit():
    response = client.put(
        "/units/foo",
        json={"unit": "foobar"},
    )
    assert response.status_code == 204

    response = client.get("/units/foo")
    assert response.status_code == 404

    response = client.get("/units/foobar")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == "foobar"


def test_patch_unit():
    response = client.patch(
        "/units/foobar",
        json={"unit": "foo"},
    )
    assert response.status_code == 204

    response = client.get("/units/foo")
    assert response.status_code == 200


def test_empty_patch_unit():
    response = client.patch("/units/foo", json={})
    assert response.status_code == 204

    response = client.get("/units/foo")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == "foo"


def test_delete_unit():
    response = client.delete("/units/foo")
    assert response.status_code == 204

    # Delete bar
    response = client.delete("/units/bar")
    assert response.status_code == 204
