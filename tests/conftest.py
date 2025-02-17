import pytest

from tests.testapp.app import create_app


@pytest.fixture()
def app():
    app_return = create_app()
    app_return.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app_return

    # clean up / reset resources here


@pytest.fixture
def test_client(app):
    """Test client for the Flask application."""
    with app.test_client() as client:
        yield client
