"""
Unit tests for lendingtree third party API
"""
from app import lendingtree_client
import pytest
import requests_mock


def test_lendingtree_api_failure():
    """
    Tests that a ConnectionError will be raised if the third party lendingtree
    API is down.
    """
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, status_code=500, text='Error from lendingtree')

        with pytest.raises(ConnectionError):
            # You cannot make any assertion on the result
            # because the request raises an exception and
            # wouldn't return anything
            lendingtree_client.business_reviews(business_url="fundbox-inc/111943337", page_num=1)
