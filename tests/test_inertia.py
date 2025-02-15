import json

from bs4 import BeautifulSoup


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
