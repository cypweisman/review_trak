"""
My API that fetches data from the lendingtree API, parses it and returns
tailored json data
"""
import json

from flask import Flask, request, abort
from lendingtree_client import LendingTreeClient
from bs4_helpers import (
    get_soup_page,
    parse_soup_tag_class,
    parse_soup_page_attr,
    BeautifulSoup
)
from bs4.element import Tag, ResultSet

app = Flask(__name__)
lendingtree_client = LendingTreeClient()



@app.route('/business_reviews', methods=['GET'])
def reviews() -> json:

    # If no business url provided, return error
    business_url = None
    if request.args.get('business_url'):
        business_url = request.args.get('business_url')
        # TODO - business_url = _parse_user_input(user_input)
    else:
        return abort(404)

    # Get landing page for business url
    landing_page = _fetch_business_review_page(business_url, page_num=1)
    soup_landing_page = get_soup_page(landing_page)

    # Get number of reviews and review pages for the business
    num_reviews, num_pages = _get_num_of_reviews_and_pages(soup_landing_page)

    # Get review details for each review on each business review page
    business_reviews = _get_business_reviews(soup_landing_page, business_url,
                                             num_reviews, num_pages)

    # Return business reviews in json format
    return business_reviews


# TODO???????????
def _parse_user_input(user_input):
    """
    """
    base_uri = lendingtree_client.base_uri
    if base_uri in user_input:
        business_url = user_input.split(base_uri)[1]
        return business_url
    else:
        return abort(404)

def _fetch_business_review_page(business_url: str, page_num: int) -> str:
    """
    Makes a web request to the lendingtree API for the given business page.

    Args:
        business_url: path to the lendingtree API business page
        page_num: page number for the business

    Return:
        fetched_page: html text of the specified business page
    """
    try:
        fetched_page = lendingtree_client.business_reviews(business_url,
                                                           page_num)
    except ConnectionError:
            abort(503)
    return fetched_page

def _get_num_of_reviews_and_pages(soup_page: BeautifulSoup,
                                  reviews_per_page: int = 10) -> tuple:
    """
    Parse the soup page for the number of reviews and calulate the total
    number of pages for the business.

    Args:
        soup_page: BeautifulSoup representation of a html business page
        reviews_per_page: max number of reviews that can appear on a business
                          page lendingtree per the lendingtree API

    Return:
        review_count, number_of_review_pages: number of reviews and number of
                                              pages for the business
    """
    # Parse soup_page for review count
    bs4_review_count = soup_page.find( class_ = "reviews-count" )
    try:
        review_count = int(str(bs4_review_count.contents[0].string).split(' ')[0])
    except ValueError:
        abort(500)

    # Calculate total number of review pages
    if review_count == 0:
        return review_count, 0
    elif review_count >0 and review_count <=10:
        return review_count, 1
    else:
        number_of_review_pages = review_count // reviews_per_page
        if review_count % reviews_per_page > 0:
            number_of_review_pages += 1
        return review_count, number_of_review_pages

def _parse_rating_number(rating_string: str) -> int:
    """
    Converts the rating string into an integer.

    Args:
        rating_string: rating in format "(5 of 5)"

    Return:
        rating_int: rating as integer
    """
    stripped_rating = rating_string.split(' of')
    rating_int = int(stripped_rating[0].split('(')[1])
    return rating_int

def _get_reviews_set(soup_page: BeautifulSoup) -> ResultSet:
    """
    Call bs4 helper to retrieve all soup_page content containing review data.

    Args:
        soup_page: BeautifulSoup representation of a html business page

    Return:
        BeautifulSoup ResultSet containing all reviews on the given soup page
    """
    return parse_soup_page_attr(soup_page, attr_name="class", attr_value="mainReviews")

def _build_review_obj(review_tag: Tag) -> dict:
    """
    Compiles a dict of parsed review data

    Args:
        review_tag: BeautifulSoup Tag containing review metadata

    Return:
        review_dict: parsed review data
    """
    review_dict = {
        "title" : parse_soup_tag_class(review_tag, 'reviewTitle'),
        "content" : parse_soup_tag_class(review_tag, 'reviewText'),
        "author" : parse_soup_tag_class(review_tag, 'consumerName'),
        "date" : parse_soup_tag_class(review_tag, 'consumerReviewDate'),
        "rating" : _parse_rating_number(parse_soup_tag_class(review_tag, 'numRec')),
    }
    return review_dict

def _get_business_reviews(soup_landing_page, business_url: str, num_reviews,
                          num_review_pages: int) -> json:
    """
    Compiles a list of dictionaries containing parsed review data for each
    review for the given business and returns it as json.

    Args:
        soup_landing_page: BeautifulSoup representation of the first html page
                           for the given business
        business_url: path to the lendingtree API business page
        page_num: page number for the business
        num_review_pages: total number of pages for the business

    Return:
        business_reviews_json: all reviews for the business or informative
                               message if none exist
    """
    if num_reviews == 0:
        return json.dumps(f'There are no reviews for business: {business_url}')

    business_reviews = []

    # Get reviews from landing page
    landing_page_reviews_set = _get_reviews_set(soup_landing_page)
    for landing_review_tag in landing_page_reviews_set:
        landing_review_data = _build_review_obj(landing_review_tag)
        business_reviews.append(landing_review_data)

    # Get reviews from any subsequent business review pages
    next_page = 2
    while next_page <= num_review_pages:
        review_page = _fetch_business_review_page(business_url, page_num=next_page)
        soup_page = get_soup_page(review_page)
        reviews_set = _get_reviews_set(soup_page)
        for review_tag in reviews_set:
            review_data = _build_review_obj(review_tag)
            business_reviews.append(review_data)
        next_page += 1

    # Return reviews
    business_reviews_json = json.dumps(business_reviews, indent=2, ensure_ascii=False).encode('utf8')
    return business_reviews_json
