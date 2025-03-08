import json

from tests.test_inertia import TestInertia


class TestPage(TestInertia):
    root = "app"
    route = "/"
    component = "component"
    expected_props = {"name": "Alice"}

    def test_inertia_initial_render(self, test_client, app):
        """Test that Inertia is available on the test client."""
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(app)

    def test_inertia_page_data(self, test_client, app):
        """Test that the Inertia response contains the correct page data."""
        response = test_client.get(self.route, headers=self.inertia_headers(app))
        assert json.loads(response.data) == self.inertia_expect(app)

    def test_version_mismatch(self, test_client):
        """Test version mismatch handling"""
        headers = {"X-Inertia": "true", "X-Inertia-Version": "wrong-version"}
        response = test_client.get(self.route, headers=headers)
        assert response.status_code == 409


class TestShorthand(TestInertia):
    root = "app"
    route = "/shorthand"
    component = "component"

    def test_inertia_initial_render(self, test_client, app):
        """Test that Inertia is available on the test client."""
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(app)

    def test_inertia_page_data(self, test_client, app):
        """Test that the Inertia response contains the correct page data."""
        response = test_client.get(self.route, headers=self.inertia_headers(app))
        assert json.loads(response.data) == self.inertia_expect(app)
