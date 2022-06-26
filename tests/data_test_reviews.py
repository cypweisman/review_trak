"""
Test data for test_reviews
"""

VALID_REVIEW_DATA = '''
<html>
<body>
<a href="#reviewBlockStart" class="reviews-count" aria-label="29 reviews for Fundbox, Inc">29 Reviews</a>
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

NO_REVIEW_DATA = '''
<html>
<body>
<a href="#reviewBlockStart" class="reviews-count" aria-label="0 reviews for Fundbox, Inc">0 Reviews</a>
</body>
</html>
'''
