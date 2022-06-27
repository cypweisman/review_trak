"""
Test data for test_reviews
"""

# Disable warning about 'too few public methods' since this is a Dataclass with no methods
# pylint: disable=R0903
class TestDataSet:
    """
    Class for coupling related/complimentary data to be used as a set
    """
    data_as_html: str
    parsed_data_resp: bytes

REVIEWS_HTML = '''
<html>
<body>
<a href="#reviewBlockStart" class="reviews-count" aria-label="2 reviews for Fundbox, Inc">2 Reviews</a>
<div class="col-xs-12 mainReviews " aria-hidden="false">
  <div class="numRec">(5 of 5)<span class="visually-hidden">stars</span></div>
      <div class="col-lg-9 col-sm-8 col-xs-12 reviewDetail">
          <p class="reviewTitle">Completely Satisfied with the service I received</p>
          <p class="reviewText">Completely Satisfied with the service I received from Katelynn.</p>
          <p class="consumerName">Nina</p>
          <p class="consumerReviewDate">Reviewed in April 2020</p>
      </div>
  </div>
</div>
<div class="col-xs-12 mainReviews " aria-hidden="false">
  <div class="numRec">(3 of 5)<span class="visually-hidden">stars</span></div>
      <div class="col-lg-9 col-sm-8 col-xs-12 reviewDetail">
          <p class="reviewTitle">Yeah it was great</p>
          <p class="reviewText">They did a nice job on everything.</p>
          <p class="consumerName">Lori</p>
          <p class="consumerReviewDate">Reviewed in January 2021</p>
      </div>
  </div>
</div>
</body>
</html>
'''

PARSED_REVIEWS_JSON = b'[\n  {\n    "title": "Completely Satisfied with the service I received",\n    "content": "Completely Satisfied with the service I received from Katelynn.",\n    "author": "Nina",\n    "date": "Reviewed in April 2020",\n    "rating": 5\n  },\n  {\n    "title": "Yeah it was great",\n    "content": "They did a nice job on everything.",\n    "author": "Lori",\n    "date": "Reviewed in January 2021",\n    "rating": 3\n  }\n]'

NO_REVIEWS_HTML = '''
<html>
<body>
<a href="#reviewBlockStart" class="reviews-count" aria-label="0 reviews for Fundbox, Inc">0 Reviews</a>
</body>
</html>
'''

NO_REVIEWS_PARSED_JSON = b'"There are no reviews for business: fundbox-inc/111943337"'

REVIEWS_DATA = TestDataSet()
REVIEWS_DATA.data_as_html, REVIEWS_DATA.parsed_data_resp = REVIEWS_HTML, PARSED_REVIEWS_JSON

NO_REVIEWS_DATA = TestDataSet()
NO_REVIEWS_DATA.data_as_html, NO_REVIEWS_DATA.parsed_data_resp = NO_REVIEWS_HTML, NO_REVIEWS_PARSED_JSON
