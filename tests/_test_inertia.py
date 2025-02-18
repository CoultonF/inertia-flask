import json

from bs4 import BeautifulSoup

from inertia_flask import _get_asset_version


def test_inertia_available(test_client):
    """Test that Inertia is available on the test client."""
    response = test_client.get("/")

    # Check that the response contains the Inertia-related content
    assert response.status_code == 200
    assert b"data-page" in response.data
    assert b'id="root"' in response.data


def test_inertia_page_data(test_client):
    """Test that the Inertia response contains the correct page data."""
    response = test_client.get("/")

    # Parse the response data
    soup = BeautifulSoup(response.data, "html.parser")
    inertia_div = soup.find("div", id="root")
    data_page = inertia_div["data-page"]

    # Expected data
    expected_data = {
        "component": "component",
        "props": {"name": "John Doe"},
        "url": "/",
        "encryptHistory": False,
        "clearHistory": False,
    }

    # Parse the data-page attribute
    parsed_data = json.loads(data_page)

    # Check that the version field is a string
    assert isinstance(parsed_data["version"], str)

    # Remove the version field from the parsed data for comparison
    del parsed_data["version"]
    assert parsed_data == expected_data


def test_inertia_defer_page(test_client):
    """Test that deferred props are correctly rendered."""
    response = test_client.get("/defer")

    # Parse the response data
    soup = BeautifulSoup(response.data, "html.parser")
    inertia_div = soup.find("div", id="root")
    data_page = inertia_div["data-page"]

    # Expected data
    expected_data = {
        "component": "deferred",
        "props": {"name": "Jane Doe"},
        "url": "/defer",
        "encryptHistory": False,
        "clearHistory": False,
        "version": _get_asset_version(),
        "deferredProps": {"default": ["deferred"]},
    }

    # Parse the data-page attribute
    parsed_data = json.loads(data_page)

    assert parsed_data == expected_data


def test_inertia_defer_resolver(app, test_client):
    """Test that deferred props are correctly resolved."""
    with app.test_request_context("/defer"):
        asset_version = _get_asset_version()
    response = test_client.get(
        "/defer",
        headers={
            "X-Inertia": "true",
            "X-Inertia-Version": asset_version,
            "X-Inertia-Partial-Data": "deferred",
            "X-Inertia-Partial-Component": "deferred",
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    # Expected data
    expected_data = {
        "component": "deferred",
        "props": {"deferred": "deferred result"},
        "url": "/defer",
        "version": asset_version,
        "encryptHistory": False,
        "clearHistory": False,
    }

    # Parse the data-page attribute
    parsed_data = json.loads(response.data)

    assert parsed_data == expected_data


def test_inertia_defer_group_page(app, test_client):
    with app.test_request_context("/defer-group"):
        asset_version = _get_asset_version()
    response = test_client.get("/defer-group")

    # Parse the response data
    soup = BeautifulSoup(response.data, "html.parser")
    inertia_div = soup.find("div", id="root")
    data_page = inertia_div["data-page"]
    expected_data = {
        "component": "defer-group",
        "props": {
            "name": "Jane Doe",
        },
        "deferredProps": {
            "default": ["deferred"],
            "group-defer": ["defer-group-value", "defer-group-other"],
        },
        "url": "/defer-group",
        "encryptHistory": False,
        "clearHistory": False,
        "version": asset_version,
    }
    # Parse the data-page attribute
    parsed_data = json.loads(data_page)

    assert parsed_data == expected_data


def test_inertia_defer_group_resolver(app, test_client):
    """Test that deferred props are correctly resolved."""
    url = "/defer-group"
    with app.test_request_context(url):
        asset_version = _get_asset_version()
    response = test_client.get(
        url,
        headers={
            "X-Inertia": "true",
            "X-Inertia-Version": asset_version,
            "X-Inertia-Partial-Data": "defer-group-value,defer-group-other",
            "X-Inertia-Partial-Component": "defer-group",
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    # Expected data
    expected_data = {
        "component": "defer-group",
        "props": {
            "defer-group-value": "group result 2",
            "defer-group-other": "other result 2",
        },
        "url": url,
        "version": asset_version,
        "encryptHistory": False,
        "clearHistory": False,
    }

    # Parse the data-page attribute
    parsed_data = json.loads(response.data)

    assert parsed_data == expected_data


def test_inertia_defer_merge_resolver(app, test_client):
    """Test that deferred props are correctly resolved."""
    url = "/defer-merge"
    with app.test_request_context(url):
        asset_version = _get_asset_version()
    response = test_client.get(
        url,
        headers={
            "X-Inertia": "true",
            "X-Inertia-Version": asset_version,
            "X-Inertia-Partial-Data": "defer-merge",
            "X-Inertia-Partial-Component": "defer-merge",
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    # Expected data
    expected_data = {
        "component": "defer-merge",
        "props": {
            "defer-merge": ["1"],
        },
        "url": url,
        "version": asset_version,
        "encryptHistory": False,
        "clearHistory": False,
        "mergeProps": [
            "defer-merge",
        ],
    }

    # Parse the data-page attribute
    parsed_data = json.loads(response.data)

    assert parsed_data == expected_data
