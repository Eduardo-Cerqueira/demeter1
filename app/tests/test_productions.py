from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_production():
    client.post(
        "/units/",
        json={"unit": "L"},
    )

    client.post(
        "/units/",
        json={"unit": "KG"},
    )

    response = client.post(
        "/productions/",
        json={"code": 500, "unit": "KG", "name": "E 500KG"},
    )
    assert response.status_code == 201

    response = client.post(
        "/productions/",
        json={"code": 200, "unit": "L", "name": "E 200L"},
    )

    assert response.status_code == 201


def test_fetch_all_productions():
    """Makes a get request in the route /productions/ to fetch all productions"""
    response = client.get("/productions/")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == [[500, "KG", "E 500KG"], [200, "L", "E 200L"]]


def test_fetch_one_production():
    """Makes a get request in the route /productions/{production} for the unit 'foo' to fetch the unit"""
    response = client.get("/productions/500")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == [500, "KG", "E 500KG"]


def test_fetch_nonexistent_production():
    """Makes a get request in the route /productions/{production} for the production code '400' to try to fetch the
    nonexistent unit"""
    response = client.get("/productions/400")
    assert response.status_code == 404


def test_put_production():
    """Makes a put request in the route /productions/{production} for the production
    unit 'L' to 'KG', name 'E 200L' to 'E 200KG'"""
    response = client.put(
        "/productions/500",
        json={"unit": "L", "name": "E 200L"},
    )
    assert response.status_code == 204

    response = client.get("/productions/500")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == [500, "L", "E 200L"]


def test_patch_production():
    """Makes a patch request in the route /productions/{production} for the production name 'E 200L' to 'EC 200L' """
    response = client.patch(
        "/productions/500",
        json={"name": "EC 200L"},
    )
    assert response.status_code == 204

    response = client.get("/productions/500")

    data = response.json()
    assert data["data"] == [500, "L", "EC 200L"]


def test_empty_patch_production():
    """Makes a patch request in the route /productions/{production} for the product code '200' with an empty payload"""
    response = client.patch("/productions/500", json={})
    assert response.status_code == 204

    response = client.get("/productions/500")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == [500, "L", "EC 200L"]


def test_delete_production():
    """Makes a delete request in the route /productions/{production} for the production code '500' """
    response = client.delete("/productions/500")
    assert response.status_code == 204

    response = client.delete("/productions/200")
    assert response.status_code == 204

    client.delete("/units/L")
    client.delete("/units/KG")
