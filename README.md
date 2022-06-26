#review_trak
============

## What It Does:
This web service will act as Third Party API for web clients who wish to
access tailored business review data from the lendingtree API. The service will
scrape the relevant pages on lendingtree for the business' review data, parse it
and return it as json.


## How It's Used:
Provide the path to the business on lendingtree, i.e.'fundbox-inc/111943337'

## Design Assumptions:
1. The web service is only intended to scrape `https://www.lendingtree.com/reviews/business`
1. No GUI is required
1. No datastore is required

## Install steps for developers
`git clone https://github.com/cypweisman/review_trak.git`

`cd review_trak`

`pip install virtualenv`

`python3 -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

`git checkout -b <new_branch_name>`

## Start the service

`source env/bin/activate`

`flask run`

## Make requests

Example request using `curl`:

`curl 'http://127.0.0.1:5000/business_reviews?business_url=fundbox-inc/111943337'`


## Run tests

`source env/bin/activate`

`pytest`
