import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.api.routes import health, files


class TestRoutesInit:
    def test_health_module_exists(self):
        assert health is not None

    def test_files_module_exists(self):
        assert files is not None
