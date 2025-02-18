from tests.test_inertia import TestInertiaPartial


class TestGroup(TestInertiaPartial):
    root = "root"
    route = "/group"
    component = "component"
    props = "email"
    expected_props = {"name": "Alice"}
    deferred_props = {"default": [props]}
    expected_deferred_props = {"email": "alice@wonderland.com"}
