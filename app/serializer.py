from flask_restful import fields

""" This module helps serialize the
data being sent to the user """
items_serializer = {
    'list_id': fields.Integer,
    'item_name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'completed': fields.Boolean
}

bucket_list_serializer = {
    'bucket_list_id': fields.Integer,
    'created_by': fields.Integer,
    'bucket_list_name': fields.String,
    'items': fields.Nested(items_serializer),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}