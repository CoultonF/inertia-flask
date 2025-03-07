import json

from tests.test_inertia import TestInertia


class TestBlueprint(TestInertia):
    """Tests related to the blueprint functionality around Inertia"""

    root = "app"
    route = "/blueprint"
    component = "component"
    expected_props = {"page": "blueprint"}

    def test_blueprint_initial_render(self, test_client, app):
        """Test that Inertia is using the blueprint template."""
        response = test_client.get(self.route)
        print(response)
        assert response.status_code == 200
        assert self.parse_page_title(response) == "Inertia Blueprint Tests"
        assert self.parse_initial_response(response) == self.inertia_expect(app)

    def test_blueprint_page_data(self, test_client, app):
        """Test that the Inertia response contains the correct page data."""
        response = test_client.get(self.route, headers=self.inertia_headers(app))
        assert json.loads(response.data) == self.inertia_expect(app)
