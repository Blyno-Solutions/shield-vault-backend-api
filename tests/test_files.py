import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestFilesEndpoints:
    def test_files_upload_docs(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "/files/upload" in schema["paths"]
    
    def test_files_download_docs(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "/files/download/{file_id}" in schema["paths"]
    
    def test_files_upload_validation(self):
        response = client.post("/files/upload")
        assert response.status_code == 422
    
    def test_files_download_validation(self):
        response = client.get("/files/download/invalid-id")
        assert response.status_code == 200