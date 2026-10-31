from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_saludo():
    response = client.get("/saludo/Ana")

    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hola, Ana"}


def test_saludo_mayusculas():
    response = client.get("/saludo/Ana?mayusculas=true")

    assert response.status_code == 200
    assert response.json() == {"mensaje": "HOLA, ANA"}


def test_cuadrado():
    response = client.get("/cuadrado/12")

    assert response.status_code == 200
    assert response.json() == {"n": 12, "cuadrado": 144}
