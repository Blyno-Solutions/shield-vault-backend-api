"""
Integration tests for Shield Vault API endpoints.
Tests HTTP endpoints using httpx with ASGITransport (no live server required).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import httpx
from httpx import ASGITransport
from typing import Generator
from app.main import app


@pytest.fixture
async def client() -> Generator:  # type: ignore
    """
    Create an async test client using ASGITransport for in-process testing.
    No live server required - runs FastAPI directly.
    """
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


class TestRootEndpoint:
    async def test_root_endpoint_exists(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert "message" in data


class TestHealthEndpoint:
    async def test_health_endpoint(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestSecurityEndpoints:
    async def test_openapi_schema_accessible(self, client):
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema

    async def test_api_docs_accessible(self, client):
        docs_response = await client.get("/docs")
        assert docs_response.status_code == 200
        assert "text/html" in docs_response.headers["content-type"]

        redoc_response = await client.get("/redoc")
        assert redoc_response.status_code == 200
        assert "text/html" in redoc_response.headers["content-type"]

        schema_response = await client.get("/openapi.json")
        assert schema_response.status_code == 200
        assert "application/json" in schema_response.headers["content-type"]


@pytest.mark.asyncio
async def test_api_health():
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200


class TestFilesEndpoint:
    async def test_files_upload_endpoint_docs(self, client):
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        paths = schema["paths"]
        assert "/files/upload" in paths

    async def test_files_download_endpoint_docs(self, client):
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        paths = schema["paths"]
        assert "/files/download/{file_id}" in paths


class TestConfigEndpoint:
    def test_config_imports(self):
        from app.core.config import settings

        assert settings is not None
