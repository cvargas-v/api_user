import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import user_collection

client = TestClient(app)

# Limpieza de base de datos antes de cada test
@pytest.fixture(autouse=True)
def clear_db():
    user_collection.delete_many({})

# Datos válidos de usuario
validacion_usuario = {
    "name": "Juan Rodriguez",
    "email": "juan@rodriguez.org",
    "password": "Hunter22",
    "phones": [
        {"number": "1234567", "citycode": "1", "contrycode": "57"}
    ]
}

def test_usuario_existoso():
    response = client.post("/users", json=validacion_usuario)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == validacion_usuario["email"]
    assert "token" in data
    assert "id" in data
    assert data["isactive"] is True

def test_email_duplicado():
    client.post("/users", json=validacion_usuario)
    response = client.post("/users", json=validacion_usuario)
    assert response.status_code == 409
    assert response.json() == {"mensaje": "El correo ya registrado"}

def test_mail_invalido():
    bad_user = validacion_usuario.copy()
    bad_user["email"] = "no-valido"
    response = client.post("/users", json=bad_user)
    assert response.status_code == 422
    assert response.json()["detail"]

def test_password_invalido():
    bad_user = validacion_usuario.copy()
    bad_user["password"] = "pass123"  # No cumple la regex
    response = client.post("/users", json=bad_user)
    assert response.status_code == 422
    assert response.json()["detail"]
