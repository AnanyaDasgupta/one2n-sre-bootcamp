# tests/test_health.py

"""
This module contains tests to verify that the health check functionality
is working correctly, ensuring the API is responsive and healthy.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthcheck():
    """
    This test verifies that the health check endpoint returns a 200 status code
    and the expected JSON response indicating the service is healthy.
    """
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}




    