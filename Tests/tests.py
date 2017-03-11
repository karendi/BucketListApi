import json
import os
import unittest
from .. import app

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SetUpTestDatabase(unittest.TestCase):
    """ setting up the test database"""
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()


class TestRegistration(unittest.TestCase):
    def setUp(self):
        """ setting up the test database """
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.drop_all()
        app.db.create_all()
        self.client = app.flask_app.test_client()

    def test_user_registration(self):
        """ Tests that checks if a user is able to register successfully"""
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkarendi5@gmail.com", "password": "password"}
        response = self.client.post("/v1/auth/register", data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_the_user_payload_being_sent(self):
        """ Tests that the payload with user data has all the required info"""
        payload = {}
        response = self.client.post("/v1/auth/register", data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_the_user_exists(self):
        """ Tests that when a user exists , they are not registered again"""
        #  register the person
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkarendi5@gmail.com", "password": "password"}
        response = self.client.post("/v1/auth/register", data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # try and register the user again the status code should be 401
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkarendi5@gmail.com", "password": "password"}
        response = self.client.post("/v1/auth/register", data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        app.db.session.remove()


class TestBucketList(unittest.TestCase):
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        response = self.client.post("/v1/auth/register", data=json.dumps(payload),
                                    content_type='application/json')
        print(response.status_code)

    def test_if_user_can_create_bucket_list(self):
        """ Test if a user can create a bucket list"""

        # generate a token for adding the data
        user_credentials = {"email": "sharonkaren@gmail.com", "password": "password"}
        auth_token = self.client.post("/auth", data=json.dumps(user_credentials),
                                      content_type='application/json')
        print(auth_token.data)

        # create a bucket list
        payload = {"bucket_list_id": 89, "bucket_list_name": "sharon", "created_by": 10012}
        response = self.client.post("/v1/bucketlists", data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)






























