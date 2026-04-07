import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the initial state
INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Fixture providing TestClient for FastAPI app with reset state"""
    # Reset activities to initial state before each test
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))
    return TestClient(app)
