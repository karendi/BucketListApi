from functools import wraps
from flask import request
from . import models
from . import db

""" Validation decorators for the data
 being posted by the user"""


def validate_user_data(func):
    """ Validates the data being posted by the user """

    @wraps(func)
    def wrapper(*args, **kwargs):
        user_data = request.get_json()
        if not user_data:
            return {"message": "bad request"}, 400
        elif "first_name" not in user_data or "last_name" not in user_data \
                or "email" not in user_data or "password" not in user_data:
            return {"message": "bad request, give the required data"}, 400
        elif user_data["first_name"] == "" or user_data["last_name"] == "" \
                or user_data["email"] == "" or user_data["password"] == "":
            return {"message": "bad request , enter all the required data"}, 400
        elif user_data["first_name"] == " " or user_data["last_name"] == " " \
                or user_data["email"] == " " or user_data["password"] == " ":
            return {"message": "bad request , enter all the required data"}, 400
        elif "@" not in user_data["email"] or "." not in user_data["email"]:
            return {"message": "invalid email provided"}, 400
        return func(*args, **kwargs)
    return wrapper


def validate_auth(func):
    """  Validates whether a user exists for token authentication"""
    @wraps(func)
    def validate_user(*args, **kwargs):
        user_credentials = request.get_json()
        if not user_credentials:
            return {"message": "You have to provide your email and password"}, 401
        elif "email" not in user_credentials or "password" not in user_credentials:
            return {"message": "You have to give the username and password"}, 401
        elif user_credentials["email"] == "" or user_credentials["password"] == "":
            return {"message": "You have to give the username and password"}, 401
        return func(*args, **kwargs)
    return validate_user


def validate_bucket_list_data(func):
    """ Validates the bucket list data"""
    @wraps(func)
    def validate_bucket_list(*args, **kwargs):
        bucket_list_data = request.get_json()
        if not bucket_list_data:
            return {"message": "You have to provide the required data"}, 400
        elif "bucket_list_id" not in bucket_list_data or "bucket_list_name" not in bucket_list_data:
            return {"message": "You have to provide the required data"}, 400
        elif bucket_list_data["bucket_list_id"] == ""or bucket_list_data["bucket_list_name"] == "":
            return {"message": "You have to provide all the required data"}, 400
        return func(*args, **kwargs)
    return validate_bucket_list


def validate_get_bucket_list_data(func):
    """ Validate the data being sent by the user for the get request """
    @wraps(func)
    def validate_data(*args, **kwargs):
        limit_of_items = request.args.get('limit')
        page_no = request.args.get('page')
        query = request.args.get('q')
        if not isinstance(limit_of_items, int):
            return {"message": "The limit must be an integer"}, 400
        elif not isinstance(page_no, int):
            return {"message":"The page number should be an integer"}, 400
        elif not isinstance(query, str):
            return {"message": "The query parameter should be a string"}, 400
        return func(*args, **kwargs)
    return validate_data


def validate_user_input_for_items(func):
    """ Validates the data that is posted for the items class post method"""
    @wraps(func)
    def validate_list_data(*args, **kwargs):
        items_data = request.json
        if "list_id" not in items_data or "item_name" not in items_data or "completed" not in items_data:
            return {"message": "You have to provide all the required information"}, 400
        elif items_data["list_id"] == "" or items_data["item_name"] == "" or items_data["completed"] == "":
            return{"message": "Enter all the required data"}, 400
        return func(*args, **kwargs)
    return validate_list_data











