import json
from abc import abstractmethod

from bs4 import BeautifulSoup

from inertia_flask import _get_asset_version


class TestInertia:
    @property
    @abstractmethod
    def root(self):
        """Subclasses must define the root attribute."""

    @property
    @abstractmethod
    def route(self):
        """Subclasses must define the route attribute."""

    @property
    @abstractmethod
    def component(self):
        """Subclasses must define the component attribute."""

    expected_props = {}

    def get_asset_version(self, app):
        with app.test_request_context(self.route):
            return _get_asset_version()

    def parse_initial_response(self, response):
        soup = BeautifulSoup(response.data, "html.parser")
        inertia_div = soup.find("div", id=self.root)
        if inertia_div is None:
            return {}
        data_page = inertia_div["data-page"]
        return json.loads(data_page)

    def inertia_headers(self, app):
        return {
            "X-Inertia": "true",
            "X-Inertia-Version": self.get_asset_version(app),
            "X-Requested-With": "XMLHttpRequest",
        }

    def inertia_expect(
        self, app, props=None, encrypt_history=False, clear_history=False
    ):
        return {
            "component": self.component,
            "props": props or self.expected_props,
            "url": self.route,
            "version": self.get_asset_version(app),
            "encryptHistory": encrypt_history,
            "clearHistory": clear_history,
        }


class TestInertiaPartial(TestInertia):
    @property
    @abstractmethod
    def props(self):
        """Subclasses must define the props attribute."""

    @property
    @abstractmethod
    def deferred_props(self):
        """Subclasses must define the props attribute."""

    def inertia_headers_partial(self, app):
        headers = super().inertia_headers(app)
        headers.update(
            {
                "X-Inertia-Partial-Data": self.props,
                "X-Inertia-Partial-Component": self.component,
            }
        )
        return headers

    def inertia_initial_expect_partial(self, app, props=None):
        expected = super().inertia_expect(app, props)
        expected["deferredProps"] = self.deferred_props or props
        return expected

    def inertia_expect_partial(self, app, props):
        expected = super().inertia_expect(app, props)
        return expected
