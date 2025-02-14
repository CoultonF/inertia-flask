import pytest

from demo.app import app, init_db


@pytest.fixture
def setup():
    """Create the setup for a test"""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_inertia_response(client):
    """Test that the route returns correct Inertia response"""
    response = client.get("/", headers={"X-Inertia": "true"})
    assert response.status_code == 200
    json_data = response.get_json()

    # Check Inertia response structure
    assert json_data["component"] == "component"
    assert "props" in json_data
    assert "value" in json_data["props"]
    assert json_data["props"]["value"] == 1

    # Check deferred data is present
    assert "posts" in json_data["props"]
