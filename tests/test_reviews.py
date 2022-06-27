"""
Unit tests for app route: /business_reviews
"""
from unittest.mock import patch
import pytest
from app import app
from .data_test_reviews import (
    REVIEWS_DATA,
    NO_REVIEWS_DATA
)

# Disable warning about names shadowing each other since fixtures must be passed as is
# pylint: disable=W0621

@pytest.fixture
def client():
    """
    Test app client
    """
    app.config['TESTING'] = True

    with app.test_client() as app_client:
        yield app_client


@pytest.fixture
def mock_get():
    """
    Patches the function requests.get in the lendingtree_client module so
    that calls to the third party API are stubbed out, enabling tests using
    the patch to provide their own response codes and data (thus exercising
    the /business_reviews logic only)
    """
    patched_get = patch('lendingtree_client.requests.get').start()
    yield patched_get

def test_business_reviews_url(mock_get, client):
    """
    Tests that the route returns the proper status code when all logic passes.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = REVIEWS_DATA.data_as_html

    url = 'https://www.lendingtree.com/reviews/business/fundbox-inc/111943337'
    response = client.get(f"business_reviews/{url}")
    assert response.status_code == 200

def test_business_reviews_no_url(client):
    """
    Tests that the route returns the proper error when no business_url is
    provided.
    """
    response = client.get("/business_reviews")
    assert response.status_code == 404

def test_business_reviews_validate_data(mock_get, client):
    """
    Validates the JSON response returned by the route.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = REVIEWS_DATA.data_as_html

    url = 'https://www.lendingtree.com/reviews/business/fundbox-inc/111943337'
    response = client.get(f"business_reviews/{url}")

    assert REVIEWS_DATA.parsed_data_resp == response.data

def test_business_reviews_no_data(mock_get, client):
    """
    Validates the JSON response returned by the route when there
    are no business reviews to be parsed.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = NO_REVIEWS_DATA.data_as_html

    url = 'https://www.lendingtree.com/reviews/business/fundbox-inc/111943337'
    response = client.get(f"business_reviews/{url}")

    assert NO_REVIEWS_DATA.parsed_data_resp == response.data
