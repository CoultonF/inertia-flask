import json

from tests.test_inertia import TestInertiaPartial


class TestDefer(TestInertiaPartial):
    root = "app"
    route = "/defer"
    component = "component"
    props = "email"
    expected_props = {"name": "Alice"}
    deferred_props = {"default": [props]}
    expected_deferred_props = {props: "alice@wonderland.com"}

    def test_inertia_initial_deferred_render(self, test_client, app):
        """test that inertia is available on the test client."""
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(
            response
        ) == self.inertia_initial_expect_partial(app)

    def test_inertia_defer_data(self, test_client, app):
        response = test_client.get(
            self.route, headers=self.inertia_headers_partial(app)
        )
        assert json.loads(response.data) == self.inertia_expect_partial(
            app, props=self.expected_deferred_props
        )
