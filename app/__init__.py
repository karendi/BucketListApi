import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list.db'
flask_app.config['JWT_SECRET_KEY'] = 'test123'


db = SQLAlchemy(flask_app)

from . import views


api = Api(flask_app)
api.add_resource(views.UserRegistration, "/v1/auth/register")
api.add_resource(views.BucketList, "/v1/bucketlists")
api.add_resource(views.SingleBucketList, "/v1/bucketlists/<int:id>")
api.add_resource(views.Items, "/v1/bucketlists/<int:id>/items")
api.add_resource(views.ItemsUpdate, "/v1/bucketlists/<int:id>/items/<int:item_id>")
jwt = JWT(flask_app, views.authenticate, views.identity)















