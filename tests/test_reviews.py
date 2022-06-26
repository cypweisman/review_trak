"""
Unit tests for app route: /business_reviews
"""
from app import app, lendingtree_client
import pytest
from unittest.mock import Mock, patch
from .data_test_reviews import VALID_REVIEW_DATA, NO_REVIEW_DATA


@pytest.fixture
def client():
  app.config['TESTING'] = True

  with app.test_client() as client:
    yield client


@pytest.fixture
def mock_get():
    """
    Patches the function requests.get in the lendingtree_client module so
    that calls to the third party API are stubbed out, enabling tests using
    the patch to provide their own response codes and data (thus exercising
    the /business_reviews logic only)
    """
    mock_get = patch('lendingtree_client.requests.get').start()
    yield mock_get


def test_business_reviews_valid(mock_get, client):
    """
    Tests that html text is probably parsed and returned by the route.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = VALID_REVIEW_DATA

    response = client.get("/business_reviews",
                          query_string={"business_url": "fundbox-inc/111943337"})
    print(response.data)
    assert b'"Yeah it was great"' in response.data

def test_business_reviews_none(mock_get, client):
    """
    Tests that html text is probably parsed and returned by the route when
    there are no business reviews in the html text.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = NO_REVIEW_DATA

    response = client.get("/business_reviews",
                          query_string={"business_url": "fundbox-inc/111943337"})
    print(response.data)
    assert b'"There are no reviews for business: fundbox-inc/111943337"' in response.data

def test_business_reviews_no_url(client):
    """
    Tests that the route returns the proper error when no business_url is
    provided.
    """
    response = client.get("/business_reviews", query_string={})
    assert response.status_code == 404
