import pytest
from fastapi.testclient import TestClient
from Backend.main import app
from Backend.database import SessionLocal, engine, Base

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_register(test_client):
    response = test_client.post("/register", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_login(test_client):
    response = test_client.post("/token", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_compute(test_client: TestClient):
    login_response = test_client.post("/token", data={"username": "testuser", "password": "password123"})
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    
    csv_content = "5,+,3\n10,-,2\n"
    
    
    response = test_client.post(
        "/api/compute",
        headers={"Authorization": f"Bearer {access_token}"},
        data={
            "request_name": "test_request",
        },
        files={
            "file": ("test.csv", csv_content, "text/csv")  # Correct way to upload file
        }
    )
    
    print("Response status code:", response.status_code)
    print("Response content:", response.json()) 
    assert response.status_code == 200


