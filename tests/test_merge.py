import json

from tests.test_inertia import TestInertiaMerge


class TestMerge(TestInertiaMerge):
    root = "app"
    route = "/merge"
    component = "component"
    props = "numbers"
    expected_props = {props: [1]}
    merge_props = [props]

    def test_inertia_initial_render(self, test_client, app):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(
            response
        ) == self.inertia_initial_expect_merge(app)

    def test_inertia_merge_data(self, test_client, app):
        response = test_client.get(
            self.route, headers=self.inertia_headers_partial(app)
        )
        assert json.loads(response.data) == self.inertia_expect_merge(app)
