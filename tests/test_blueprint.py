import json

import pytest

from inertia_flask import Inertia, InertiaInitializationError
from tests.test_inertia import TestInertia


class TestBlueprint(TestInertia):
    """Tests related to the blueprint functionality around Inertia"""

    root = "app"
    route = "/blueprint"
    component = "component"
    blueprint = "bp"
    expected_props = {"page": "blueprint"}

    def test_blueprint_initial_render(self, test_blueprint, bp):
        """Test that Inertia is using the blueprint template."""
        response = test_blueprint.get(self.route)
        assert response.status_code == 200
        assert self.parse_page_title(response) == "Inertia Blueprint Tests"
        assert self.parse_initial_response(response) == self.inertia_expect(bp)

    def test_blueprint_page_data(self, test_blueprint, bp):
        """Test that the Inertia response contains the correct page data."""
        response = test_blueprint.get(self.route, headers=self.inertia_headers(bp))
        assert json.loads(response.data) == self.inertia_expect(bp)

    def test_blueprint_version_mismatch(self, test_blueprint):
        """Test version mismatch handling"""
        headers = {"X-Inertia": "true", "X-Inertia-Version": "wrong-version"}
        response = test_blueprint.get(self.route, headers=headers)
        assert response.status_code == 409

    def test_flask_blueprint_init(self, bp):
        """Test that initializing Inertia on both app and blueprint raises an error"""
        inertia_ext = Inertia()
        with pytest.raises(InertiaInitializationError) as excinfo:
            inertia_ext.init_app(bp)
        assert "Inertia is already initialized" in str(excinfo.value)
