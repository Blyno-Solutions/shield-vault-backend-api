import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies.auth import get_current_user
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

client = TestClient(app)


async def mock_get_current_user():
    return {"id": 1, "username": "testuser", "role": "user"}


app.dependency_overrides[get_current_user] = mock_get_current_user


def create_mock_file(id=1, filename="test.txt", owner_id=1):
    mock_file = MagicMock()
    mock_file.id = id
    mock_file.filename = filename
    mock_file.file_path = "/uploads/test.txt"
    mock_file.file_size = 1024
    mock_file.mime_type = "text/plain"
    mock_file.owner_id = owner_id
    mock_file.created_at = datetime.now()
    mock_file.updated_at = datetime.now()
    mock_file.expires_at = None
    mock_file.is_deleted = 0
    return mock_file


@pytest.fixture
def mock_repo():
    with patch("app.api.routes.file_routes.FileRepository") as mock:
        repo_instance = AsyncMock()
        mock.return_value = repo_instance
        yield repo_instance


class TestFileRoutes:
    def test_create_file_success(self, mock_repo):
        mock_repo.get_by_filename = AsyncMock(return_value=None)
        mock_repo.create = AsyncMock(return_value=create_mock_file())

        response = client.post(
            "/files/",
            json={
                "filename": "test.txt",
                "file_path": "/uploads/test.txt",
                "file_size": 1024,
                "mime_type": "text/plain",
                "owner_id": 1,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["owner_id"] == 1

    def test_create_file_duplicate(self, mock_repo):
        mock_repo.get_by_filename = AsyncMock(return_value=MagicMock())

        response = client.post(
            "/files/",
            json={
                "filename": "test.txt",
                "file_path": "/uploads/test.txt",
                "file_size": 1024,
                "owner_id": 1,
            },
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_file_wrong_owner(self, mock_repo):
        response = client.post(
            "/files/",
            json={
                "filename": "test.txt",
                "file_path": "/uploads/test.txt",
                "file_size": 1024,
                "owner_id": 2,
            },
        )

        assert response.status_code == 403
        assert "Cannot create file for another user" in response.json()["detail"]

    def test_get_file_success(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=create_mock_file())

        response = client.get("/files/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["filename"] == "test.txt"

    def test_get_file_not_found(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        response = client.get("/files/999")
        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

    def test_get_file_unauthorized(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=create_mock_file(owner_id=2))

        response = client.get("/files/1")
        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]

    def test_list_user_files(self, mock_repo):
        mock_files = [
            create_mock_file(id=1, filename="test1.txt"),
            create_mock_file(id=2, filename="test2.txt"),
        ]
        mock_repo.get_by_owner = AsyncMock(return_value=mock_files)
        mock_repo.count_by_owner = AsyncMock(return_value=2)

        response = client.get("/files/?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["files"]) == 2
        assert data["files"][0]["filename"] == "test1.txt"

    def test_update_file_success(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=create_mock_file())
        mock_updated = create_mock_file(filename="updated.txt")
        mock_repo.update = AsyncMock(return_value=mock_updated)

        response = client.put("/files/1", json={"filename": "updated.txt"})
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "updated.txt"

    def test_update_file_not_found(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        response = client.put("/files/999", json={"filename": "updated.txt"})
        assert response.status_code == 404

    def test_delete_file_success(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=create_mock_file())
        mock_repo.delete = AsyncMock(return_value=True)

        response = client.delete("/files/1")
        assert response.status_code == 200
        assert response.json()["message"] == "File deleted successfully"

    def test_delete_file_not_found(self, mock_repo):
        mock_repo.get_by_id = AsyncMock(return_value=None)

        response = client.delete("/files/999")
        assert response.status_code == 404

    def test_search_files(self, mock_repo):
        mock_files = [create_mock_file()]
        mock_repo.search_by_name = AsyncMock(return_value=mock_files)

        response = client.get("/files/search/?q=test")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["filename"] == "test.txt"
