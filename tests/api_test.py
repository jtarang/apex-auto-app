import pytest
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

from api_server.models import Base

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DB_CERT_CA_PATH"] = "dummy.ca"
os.environ["DB_CLIENT_CERT_PATH"] = "dummy.cert"
os.environ["DB_CLIENT_KEY_PATH"] = "dummy.key"

TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# 2. Dependency Override Function
# This generator replaces the real DatabaseManager.get_db_session()
def override_get_db_session() -> Generator[Session, None, None]:
    """Provides a fresh database session for a test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Assuming the user's application code is in 'main.py'
from api_server import apex_auto_api as main_app

# The original api_server setup uses:
# - database_manager (from handlers/database.py)
# - vehicle_crud (from models.py, initialized in main.py)

# Override the api_server's database dependency to use the test session factory
main_app.app.dependency_overrides[main_app.database_manager.get_db_session] = override_get_db_session


# 4. Fixture for Synchronous Client and Database Setup
@pytest.fixture(scope="module")
def client() -> Generator[Client, None, None]:
    """Initializes the synchronous test client and sets up the database."""

    Base.metadata.create_all(bind=test_engine)

    # Use synchronous httpx Client
    with Client(app=main_app.app, base_url="http://test") as c:
        yield c

    # Drop all tables after tests are done (for a clean module scope)
    Base.metadata.drop_all(bind=test_engine)


# --- 3. Test Functions (CRUD Operations) ---

# Test data used across multiple tests
VEHICLE_DATA = {"make": "Tesla", "model": "Model 3", "year": 2023, "color": "Red", "is_available": True}
VEHICLE_DATA_2 = {"make": "Ford", "model": "Mustang", "year": 1969, "color": "Blue", "is_available": False}


def test_create_vehicle(client: Client):
    """Test POST /vehicles/ endpoint."""
    response = client.post("/vehicles/", json=VEHICLE_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["make"] == VEHICLE_DATA["make"]
    assert "id" in data
    assert data["id"] == 1


def test_read_vehicles_and_create_second(client: Client):
    """Test GET /vehicles/ (list) and create a second vehicle."""

    # Check the first vehicle exists
    response = client.get("/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["model"] == VEHICLE_DATA["model"]

    # Create the second vehicle
    response_2 = client.post("/vehicles/", json=VEHICLE_DATA_2)
    assert response_2.status_code == 201
    assert response_2.json()["id"] == 2

    # Check the list now has two vehicles
    response = client.get("/vehicles/")
    assert len(response.json()) == 2


def test_read_vehicle_by_id(client: Client):
    """Test GET /vehicles/{vehicle_id} endpoint."""
    # Read vehicle with ID 2 (Mustang)
    response = client.get("/vehicles/2")
    assert response.status_code == 200
    data = response.json()
    assert data["make"] == VEHICLE_DATA_2["make"]
    assert data["year"] == VEHICLE_DATA_2["year"]
    assert data["id"] == 2


def test_read_non_existent_vehicle(client: Client):
    """Test GET for a vehicle that doesn't exist."""
    response = client.get("/vehicles/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


def test_update_vehicle(client: Client):
    """Test PATCH /vehicles/{vehicle_id} endpoint."""
    # Update the color and availability of vehicle with ID 1 (Tesla)
    UPDATE_PAYLOAD = {"color": "Midnight Silver", "is_available": False}
    response = client.patch(
        "/vehicles/1",
        json=UPDATE_PAYLOAD
    )
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == UPDATE_PAYLOAD["color"]
    assert data["is_available"] == UPDATE_PAYLOAD["is_available"]
    assert data["model"] == VEHICLE_DATA["model"]  # Ensure unchanged fields are correct


def test_update_non_existent_vehicle(client: Client):
    """Test PATCH for a vehicle that doesn't exist."""
    response = client.patch(
        "/vehicles/999",
        json={"color": "Red"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


def test_delete_vehicle(client: Client):
    """Test DELETE /vehicles/{vehicle_id} endpoint."""
    # Delete the vehicle with ID 2 (Mustang)
    response = client.delete("/vehicles/2")
    assert response.status_code == 204

    # Verify it was deleted
    check_response = client.get("/vehicles/2")
    assert check_response.status_code == 404

    # Ensure ID 1 is still present
    check_response_1 = client.get("/vehicles/1")
    assert check_response_1.status_code == 200


def test_delete_non_existent_vehicle(client: Client):
    """Test DELETE for a vehicle that doesn't exist."""
    response = client.delete("/vehicles/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}