"""
Class that issues web requests to the lendingtree third party API.
"""
import requests


class LendingTreeClient:
    def __init__(self, base_uri='https://www.lendingtree.com/reviews/business/'):
        self.base_uri = base_uri

    def business_reviews(self, business_url: str, page_num: int) -> str:
        """
        Makes a GET request to lendingtree for the specified business page.

        Args:
            business_url: path to the business page
            page_num: page number for the business

        Return:
            html text of the specified business page
        """
        return self._get(business_url, params={'page_num': page_num})

    def _get(self, path: str, params: dict) -> str:
        """
        Makes GET request to lendingtree.

        Args:
            path: url path
            req_params: query parameters

        Return:
            response html text
        """
        url = self.base_uri + path
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f'Error returned from lendingtree: {response.status_code}')
        return response.text
