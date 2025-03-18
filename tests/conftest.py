import pytest

from tests.testapp.app import create_app, create_blueprint, create_share_app


@pytest.fixture()
def app():
    app_return = create_app()
    yield app_return


@pytest.fixture()
def bp():
    app_return = create_blueprint()
    yield app_return


@pytest.fixture()
def share():
    app_return = create_share_app()
    yield app_return

@pytest.fixture
def test_client(app):
    """Test client for the Flask application."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_blueprint(bp):
    """Test client for the Flask application."""
    with bp.test_client() as client:
        yield client


@pytest.fixture
def test_share(share):
    """Test client for the Flask application."""
    with share.test_client() as client:
        yield client
