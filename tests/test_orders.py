import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import OrderRepository, get_repo


@pytest.fixture
def client():
    repo = OrderRepository()
    app.dependency_overrides[get_repo] = lambda: repo

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_order_calculates_total_and_status(client):
    response = client.post(
        "/orders",
        json={
            "cliente": "Ana López",
            "producto": "Teclado",
            "cantidad": 2,
            "precio_unitario": 350.0,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["total"] == 700.0
    assert data["status"] == "pendiente"
    assert data["id"] == 1


def test_invalid_quantity_returns_422(client):
    response = client.post(
        "/orders",
        json={
            "cliente": "Ana López",
            "producto": "Teclado",
            "cantidad": 0,
            "precio_unitario": 350.0,
        },
    )

    assert response.status_code == 422


def test_missing_order_returns_404(client):
    response = client.get("/orders/999")

    assert response.status_code == 404


def test_list_update_delete(client):
    client.post(
        "/orders",
        json={
            "cliente": "Ana López",
            "producto": "Teclado",
            "cantidad": 2,
            "precio_unitario": 350.0,
        },
    )

    client.post(
        "/orders",
        json={
            "cliente": "Luis Pérez",
            "producto": "Mouse",
            "cantidad": 1,
            "precio_unitario": 200.0,
        },
    )

    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.put(
        "/orders/1",
        json={
            "cliente": "Ana López",
            "producto": "Teclado",
            "cantidad": 3,
            "precio_unitario": 350.0,
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1050.0

    response = client.delete("/orders/2")
    assert response.status_code == 204

    response = client.get("/orders/2")
    assert response.status_code == 404
    