from tests.test_inertia import TestInertia


class TestEncryptDecorator(TestInertia):
    root = "app"
    component = "component"
    route = "/encrypt-decorator"

    def test_encrypt(self, app, test_client):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(
            app, encrypt_history=True
        )


class TestEncryptFunction(TestInertia):
    root = "app"
    component = "component"
    route = "/encrypt-function"

    def test_encrypt(self, app, test_client):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(
            app, encrypt_history=True
        )


class TestClearFunction(TestInertia):
    root = "app"
    component = "component"
    route = "/clear-function"

    def test_clear(self, app, test_client):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(
            app, clear_history=True
        )


class TestClearDecorator(TestInertia):
    root = "app"
    component = "component"
    route = "/clear-decorator"

    def test_clear(self, app, test_client):
        response = test_client.get(self.route)
        assert response.status_code == 200
        assert self.parse_initial_response(response) == self.inertia_expect(
            app, clear_history=True
        )
