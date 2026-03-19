import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    def test_health_root(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert data["database"] == "connected"

    def test_health_ping(self):
        response = client.get("/health/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong"}

    def test_health_ready(self):
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True
        assert "checks" in data
