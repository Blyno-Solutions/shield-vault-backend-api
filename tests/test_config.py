import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app.core.config import settings

class TestConfig:
    def test_settings_load(self):
        assert settings.DATABASE_URL is not None
        assert settings.SECRET_KEY is not None
    
    def test_settings_attributes(self):
        assert hasattr(settings, "DATABASE_URL")
        assert hasattr(settings, "SECRET_KEY")
        assert hasattr(settings, "ENCRYPTION_KEY")
        assert hasattr(settings, "POSTGRES_USER")
        assert hasattr(settings, "POSTGRES_PASSWORD")
        assert hasattr(settings, "POSTGRES_DB")