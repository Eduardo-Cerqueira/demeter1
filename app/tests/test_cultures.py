from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_culture():
    client.post(
        "/units/",
        json={"unit": "L"},
    )

    client.post(
        "/productions/",
        json={"code": 200, "unit": "L", "name": "E 200L"},
    )

    client.post(
        "/plots/",
        json={"number": 50, "surface": 100, "name": "Foo Bar", "location": "foobar"},
    )

    response = client.post(
        "/cultures/",
        json={
            "plot_number": 50,
            "production_code": 200,
            "start_date": "2023-01-01",
            "end_date": "2023-02-01",
            "quantity": 300,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/cultures/",
        json={
            "plot_number": 50,
            "production_code": 200,
            "start_date": "2023-10-01",
            "end_date": "2023-11-01",
            "quantity": 500,
        },
    )

    assert response.status_code == 201


def test_fetch_all_cultures():
    """Makes a get request in the route /cultures/ to fetch all cultures"""
    response = client.get("/cultures/")
    assert response.status_code == 200

    data = response.json()
    first_culture = data["data"][0]
    second_culture = data["data"][1]

    assert first_culture == [first_culture[0], 50, 200, "2023-01-01", "2023-02-01", 300]

    assert second_culture == [
        second_culture[0],
        50,
        200,
        "2023-10-01",
        "2023-11-01",
        500,
    ]


def test_fetch_one_culture():
    """Makes a get request in the route /cultures/{culture}"""
    response = client.get("/cultures/")
    data = response.json()
    culture_uuid = data["data"][0][0]

    response = client.get(f"/cultures/{culture_uuid}")
    assert response.status_code == 200

    data = response.json()
    assert data["data"] == [culture_uuid, 50, 200, "2023-01-01", "2023-02-01", 300]


def test_delete_production():
    """Makes a delete request in the route /productions/{production} for the culture"""

    response = client.get("/cultures/")
    data = response.json()

    response = client.delete(f"/cultures/{data['data'][0][0]}")
    assert response.status_code == 204

    response = client.delete(f"/cultures/{data['data'][1][0]}")
    assert response.status_code == 204

    client.delete("/plots/50")

    client.delete("/productions/200")

    client.delete("/units/L")
