import datetime
from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt import jwt_required, current_identity
from .decorators import validate_user_data, validate_bucket_list_data, validate_get_bucket_list_data,\
    validate_user_input_for_items
from .serializer import bucket_list_serializer
from . import models
from . import db


def authenticate(username, password):
    """ Verifies that the email and password
     match and returns a token"""
    user = db.session.query(models.UserModel).filter_by(email=username).first()
    if user and user.verify_password(password):  # check if the user exists and the password is correct
        return user


def identity(payload):
    """ Sets the current identity to the user_id
    of the user that is logged in"""
    user_id = payload['identity']
    return db.session.query(models.UserModel).filter_by(user_id=user_id).first()


class UserRegistration(Resource):
    """ Registers new users and validates data
    using the validate_user_data"""
    @validate_user_data
    def post(self):
        user_data = request.json
        user_first_name = user_data.get("first_name")
        user_last_name = user_data.get("last_name")
        user_email = user_data.get("email")
        user_password = user_data.get("password")

        # check if the user exists
        existing_user = db.session.query(models.UserModel).filter_by(email=user_email).first()
        if existing_user is None:
            try:
                new_user = models.UserModel(
                    first_name=user_first_name,
                    last_name=user_last_name,
                    email=user_email,
                    password=user_password
                )
                new_user.hash_password(user_password)
                db.session.add(new_user)
                db.session.commit()
                return {"message": "The user has been added successfully"}, 201

            except Exception as e:
                return str(e)
        else:
            return {"message": "The user already exists"}, 401


class BucketList(Resource):
    """ CRUD functions for bucket list items
    Use auth.login_required for authorization """
    @jwt_required()
    @validate_bucket_list_data
    def post(self):
        bucket_list_data = request.json
        bucket_list_id = bucket_list_data.get('bucket_list_id')
        bucket_list_name = bucket_list_data.get('bucket_list_name')

        # check if the bucket list with the same id exists
        check_bucket_list = db.session.query(models.BucketList).filter_by(bucket_list_id=bucket_list_id).first()
        if check_bucket_list is not None:
            return {"message": "You can not enter a bucket list with a duplicated Id"}, 401
        else:
            try:
                new_bucket_list = models.BucketList(bucket_list_id=bucket_list_id,
                                                    bucket_list_name=bucket_list_name,
                                                    created_by=current_identity.user_id
                                                    )
                db.session.add(new_bucket_list)
                db.session.commit()
                return {"message": "You have created a new bucket list"}, 201

            except Exception as e:
                return str(e)

    @jwt_required()
    @validate_get_bucket_list_data
    @marshal_with(bucket_list_serializer)
    def get(self):
        """ Returns all the bucket list items from the database
         and has the option of pagination """

        # pick the parameters from the url
        limit_of_items = request.args.get('limit')
        page_no = request.args.get('page')
        query = request.args.get('q')
        if query:
            """ if a user wants to search for a specific bucket list"""
            bucket_list_results_pagination = models.BucketList.query.filter(models.BucketList.bucket_list_name.like(
                '%' + query + '%')).filter_by(created_by=current_identity.user_id).paginate(int(page_no),
                                                                                            int(limit_of_items), False)
            if bucket_list_results_pagination:
                buckets = bucket_list_results_pagination.items
                bkts = [bucket for bucket in buckets]
                return bkts, 200
            else:
                return {"message": "Bucket List '{0}'can not be found".format(query)}, 404
        else:
            """ Returns all the bucket list"""
            all_bucket_list_results = models.BucketList.query.filter_by(created_by=current_identity.user_id).\
                paginate(int(page_no), int(limit_of_items), False)
            if all_bucket_list_results:
                buckets = all_bucket_list_results.items
                bkts = [bucket for bucket in buckets]
                return bkts, 200
            else:
                return {"message": "Bucket Lists can not be found"}, 404


class SingleBucketList(Resource):
    @jwt_required()
    @marshal_with(bucket_list_serializer)
    def get(self,id):
        """ gets a single bucket list """
        bucket_list = db.session.query(models.BucketList).get(id)
        if bucket_list is None:
            return {"message": "The bucket list does not exist"}, 404
        return 200

    @jwt_required()
    def delete(self, id):
        """ deletes a given bucket list """
        # pick the id of the bucket list
        bucket_list_id = id

        delete_bucket_list = db.session.query(models.BucketList).get(bucket_list_id)
        if delete_bucket_list is None:
            return {"message": "The bucket list does not exist"}, 404
        else:
            db.session.delete(delete_bucket_list)
            db.session.commit()
            return {"message": "The bucket list has been deleted successfully "}, 200


class Items(Resource):
    @jwt_required()
    @validate_user_input_for_items
    def post(self, id):
        bucket_list_id = id
        items_data = request.json
        item_id = items_data.get('list_id')
        item_name = items_data.get('item_name')
        completed = items_data.get('completed')

        # check if the bucket_list exists
        existing_bucket_list = db.session.query(models.BucketList).get(id)
        if existing_bucket_list is None:
            return {"message": "The bucket list does not exist, so you can't add an item"}, 401
        else:
            # check if the item exists
            existing_item = db.session.query(models.Items).get(item_id)
            if existing_item is not None:
                return {"message": "An item with the same ID already exists"}, 401
            else:
                try:
                    new_item = models.Items(list_id=item_id,
                                            item_name=item_name,
                                            bucket_list=bucket_list_id,
                                            completed=completed
                                            )
                    db.session.add(new_item)
                    db.session.commit()
                    return {"message": "The item has been created"}, 201
                except Exception as e:
                    return str(e)


class ItemsUpdate(Resource):
    @jwt_required()
    def put(self, id, item_id):
        bucket_list_id = id
        item_id = item_id
        update_data = request.json
        if update_data:
            if "item_name" in update_data:
                new_item_name = update_data.get("item_name")
            else:
                new_item_name = None
            if "completed" in update_data:
                new_status = update_data.get("completed")
            else:
                new_status = None

            # check if the item exists
            existing_item = models.Items.query.filter_by(bucket_list=bucket_list_id, list_id=item_id).first()
            if existing_item is None:
                return {"message": "The item does not exist"}, 401
            else:
                try:
                    existing_item.item_name = new_item_name
                    existing_item.completed = new_status
                    existing_item.date_modified = datetime.datetime.utcnow()
                    db.session.commit()
                    return {"message": "The item was edited successfully"}, 200

                except Exception as e:
                    return str(e)

        else:
            return {"message": "You have to enter data"}, 400

    @jwt_required()
    def delete(self, id, item_id):
        # check for the item
        bucket_list_id = id
        item_id = item_id

        existing_item = models.Items.query.filter_by(bucket_list=bucket_list_id, list_id=item_id).first()
        if existing_item is None:
            return {"message":"The item does not exist"}, 401
        else:
            try:
                db.session.delete(existing_item)
                db.session.commit()
                return {"message": "The item has been deleted"}, 200
            except Exception as e:
                str(e)