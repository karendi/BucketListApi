[![CircleCI](https://circleci.com/gh/karendi/BucketListApi/tree/develop.svg?style=svg)](https://circleci.com/gh/karendi/BucketListApi/tree/develop)

Bucket List is a list of things that one has not done before but wants to do before dying.This is
an API for an online Bucket List service that has been developed using Flask.


ENDPOINTS
------------------------------------------------------------------------------
POST /auth/login                          Logs a user in
POST /auth/register                       Register a user
POST /bucketlists/                        Create a new bucket list
GET /bucketlists/                         List all the created bucket lists
GET /bucketlists/<id>                     Get single bucket list
PUT /bucketlists/<id>                     Update this bucket list
DELETE /bucketlists/<id>                  Delete this single bucket list
POST /bucketlists/<id>/items/             Create a new item in bucket list
PUT /bucketlists/<id>/items/<item_id>     Update a bucket list item
DELETE /bucketlists/<id>/items/<item_id>  Delete an item in a bucket list