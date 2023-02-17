import json
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_cities_with_valid_input():
    response = client.get("/municipalities?department=64&rent=800&surface=50")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data["cities"]) == 5
    assert all(city.get("name") for city in data["cities"])
    assert all(city.get("postal_code") for city in data["cities"])
    assert all(city.get("rent") for city in data["cities"])
    assert all(city.get("rating") for city in data["cities"])
    assert all(city.get("population") for city in data["cities"])

def test_get_cities_with_invalid_department():
    response = client.get("/municipalities?department=999&rent=800&surface=50")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Invalid department code"

def test_get_cities_with_negative_rent():
    response = client.get("/municipalities?department=64&rent=-800&surface=50")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Rent value must be positive"

def test_get_cities_with_negative_surface():
    response = client.get("/municipalities?department=64&rent=800&surface=-50")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Surface value must be positive"

def test_get_cities_with_high_rent_value():
    response = client.get("/municipalities?department=64&rent=10000&surface=50")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Rent value exceeds maximum allowed value"

def test_get_cities_with_high_surface_value():
    response = client.get("/municipalities?department=64&rent=800&surface=2000")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Surface value exceeds maximum allowed value"

def test_get_cities_with_missing_parameters():
    response = client.get("/municipalities?department=64&rent=800")
    assert response.status_code == 422
    data = json.loads(response.content)
    assert data["detail"] == "Missing required parameters"