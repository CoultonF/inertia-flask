import pytest

from demo.app import app, init_db


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_inertia_page_render(client):
    """Test Inertia.js page rendering"""
    # Test initial page load (HTML)
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data
    assert b'id="root"' in response.data

    # Test Inertia JSON response
    headers = {"X-Inertia": "true"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()

    # Verify Inertia response structure
    assert "component" in data
    assert "props" in data
    assert "url" in data
    assert "version" in data

    # Test component and props
    assert data["component"] == "component"
    assert "value" in data["props"]
    assert data["props"]["value"] == 1


def test_inertia_partial_reload(client):
    """Test Inertia.js partial reloads"""
    headers = {
        "X-Inertia": "true",
        "X-Inertia-Partial-Data": "value",
        "X-Inertia-Partial-Component": "component",
    }

    response = client.get("/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()

    # Only requested data should be present
    assert "value" in data["props"]
    assert "defer" not in data["props"]


def test_inertia_version_mismatch(client):
    """Test Inertia.js version mismatch handling"""
    headers = {"X-Inertia": "true", "X-Inertia-Version": "invalid-version"}

    response = client.get("/", headers=headers)
    assert response.status_code == 409  # Conflict status
