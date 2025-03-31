import json

from tests.test_inertia import TestInertiaPartial


class TestPage(TestInertiaPartial):
    root = "app"
    route = "/share"
    component = "component"
    props = "email"
    expected_props = {"name": "Alice", "auth": {"user_id": "123"}}
    deferred_props = {"default": [props]}
    expected_deferred_props = {props: "alice@wonderland.com"}

    def test_inertia_initial_render(self, test_share, share):
        """Test that Inertia is available on the test client."""
        response = test_share.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_initial_expect_partial(share)

    def test_inertia_page_data(self, test_share, share):
        """Test that the Inertia response contains the correct page data."""
        response = test_share.get(self.route, headers=self.inertia_headers(share))
        assert json.loads(response.data) == self.inertia_initial_expect_partial(share)

    def test_version_mismatch(self, test_share):
        """Test version mismatch handling"""
        headers = {"X-Inertia": "true", "X-Inertia-Version": "wrong-version"}
        response = test_share.get(self.route, headers=headers)
        assert response.status_code == 409

    def test_inertia_initial_deferred_render(self, test_share, share):
        """test that inertia is available on the test client."""
        response = test_share.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(
            response
        ) == self.inertia_initial_expect_partial(share)

    def test_inertia_defer_data(self, test_share, share):
        response = test_share.get(
            self.route, headers=self.inertia_headers_partial(share)
        )
        assert json.loads(response.data) == self.inertia_expect_partial(
            share, props=self.expected_deferred_props
        )