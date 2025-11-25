#!/usr/bin/env python3

import pytest
import requests

# Define the base URL of the localhost API (modify if necessary)
BASE_URL = "http://localhost:8080"

# Test user to use as input (example: octocat)
TEST_USER = "octocat"

@pytest.fixture
def user_url():
    """
    Function to return the URL for the user endpoint.
    """
    return f"{BASE_URL}/{TEST_USER}"

def test_user_api_status(user_url):
    """
    Test to ensure the API responds with a status code of 200.
    """
    response = requests.get(user_url, timeout=60)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

def test_user_api_data(user_url):
    """
    Test to check if the API returns the correct user data for user passed  for eg: 'octocat'.
    """
    response = requests.get(user_url,timeout=60)
    data = response.json()

    # Check that the response is a list
    assert isinstance(data, list), f"Expected a list, but got {type(data)}"

    for user in data:
        assert "login" in user, "Login field is missing in user object"
        assert "id" in user, "ID field is missing in user object"
        # Further checks specific to the user "octocat" (example)
        assert user["login"] == "octocat", f"Expected login 'octocat', but got {data['login']}"

    # # Optional: If you expect only one user in the list
    # assert len(data) == 1, f"Expected one user in the list, but got {len(data)}"
def test_user_api_content_type(user_url, timeout=60):
    """
    Test to ensure the content type returned by the API is JSON.
    """
    response = requests.get(user_url)
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected 'application/json', but got {response.headers['Content-Type']}"
