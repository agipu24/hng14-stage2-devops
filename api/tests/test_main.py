import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

mock_redis = MagicMock()

with patch.dict('sys.modules', {'redis': MagicMock(Redis=MagicMock(return_value=mock_redis))}):
    from api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_create_job():
    mock_redis.lpush = MagicMock()
    mock_redis.hset = MagicMock()
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_job_not_found():
    mock_redis.hget = MagicMock(return_value=None)
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 200
    assert response.json() == {"error": "not found"}


def test_get_job_found():
    mock_redis.hget = MagicMock(return_value=b"completed")
    response = client.get("/jobs/test-123")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
