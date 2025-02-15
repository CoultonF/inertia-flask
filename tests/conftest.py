import pytest

from tests.testapp.app import create_app


@pytest.fixture
def test_client():
    """Test client for the Flask application."""
    app = create_app()
    with app.test_client() as client:
        yield client
