import json

from tests.test_inertia import TestInertiaPartial


class TestGroup(TestInertiaPartial):
    root = "app"
    route = "/group"
    component = "component"
    props = "email,phone"
    _split = props.split(",")
    expected_props = {"name": "Alice"}
    deferred_props = {"contact": _split}
    expected_deferred_props = {
        _split[0]: "alice@wonderland.com",
        _split[1]: "1234567890",
    }

    def test_inertia_initial_deferred_render(self, test_client, app):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(
            response
        ) == self.inertia_initial_expect_partial(app)

    def test_inertia_defer_group_data(self, test_client, app):
        response = test_client.get(
            self.route, headers=self.inertia_headers_partial(app)
        )
        assert json.loads(response.data) == self.inertia_expect_partial(
            app, props=self.expected_deferred_props
        )
