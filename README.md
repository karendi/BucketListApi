[![CircleCI](https://circleci.com/gh/karendi/BucketListApi/tree/develop.svg?style=svg)](https://circleci.com/gh/karendi/BucketListApi/tree/develop)

Bucket List is a list of things that one has not done before but wants to do before dying.This is
an API for an online Bucket List service that has been developed using Flask.


ENDPOINTS
------------------------------------------------------------------------------
    1. POST /auth/login                          Logs a user in
    2. POST /auth/register                       Register a user
    3. POST /bucketlists/                        Create a new bucket list
    4. GET /bucketlists/                         List all the created bucket lists
    5. GET /bucketlists/<id>                     Get single bucket list
    6. PUT /bucketlists/<id>                     Update this bucket list
    7. DELETE /bucketlists/<id>                  Delete this single bucket list
    8. POST /bucketlists/<id>/items/             Create a new item in bucket list
    9. PUT /bucketlists/<id>/items/<item_id>     Update a bucket list item
    10.DELETE /bucketlists/<id>/items/<item_id>  Delete an item in a bucket list