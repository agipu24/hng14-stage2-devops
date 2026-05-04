import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Mock redis before importing app
import sys
sys.modules['redis'] = MagicMock()

from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}

def test_create_job():
    with patch('api.main.r') as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()

def test_get_job_found():
    with patch('api.main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=b"completed")
        response = client.get("/jobs/test-123")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

def test_get_job_not_found():
    with patch('api.main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=None)
        response = client.get("/jobs/nonexistent")
        assert response.status_code == 200
        assert response.json() == {"error": "not found"}
