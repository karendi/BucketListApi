import json
import os
import unittest
from flask import url_for
from .. import app

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseTestCase(unittest.TestCase):
    """ setting up the test database"""
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        self.client.post("/v1/auth/register", data=json.dumps(payload), content_type='application/json')

        # get auth token
        payload = {"username": "sharonkaren@gmail.com", "password": "password"}
        token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
        self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']


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
        app.flask_app.config['SERVER_NAME'] = '127.0.0.0'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        self.client.post("/v1/auth/register", data=json.dumps(payload), content_type='application/json')

        # get auth token
        payload = {"username": "sharonkaren@gmail.com", "password": "password"}
        token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
        self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']

    def test_if_user_can_create_bucket_list(self):
        """ Test if a user can create a bucket list"""

        # create a bucket list

        payload = {"bucket_list_id": 89, "bucket_list_name": "sharon", "created_by": 10012}
        response = self.client.post("/v1/bucketlists", data=json.dumps(payload),
                                    headers={'Content-Type': 'application/json', 'Authorization': self.token})
        self.assertEqual(response.status_code, 201)

    def test_if_user_can_get_bucket_lists(self):
        """ Test if a user can get bucket lists """
        with app.flask_app.app_context():
            response = self.client.get(url_for('get_and_post_get_bucket_list', limit=1, page=1),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 200)


class TestSingleBucketList(BaseTestCase):
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.flask_app.config['SERVER_NAME'] = '127.0.0.0'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        self.client.post("/v1/auth/register", data=json.dumps(payload), content_type='application/json')

        # get auth token
        payload = {"username": "sharonkaren@gmail.com", "password": "password"}
        token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
        self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']

    def test_if_the_user_cant_get_a_bucket_list_if_it_does_not_exist(self):
        """ Test if the user can not get a single bucket list if it does not exist """
        with app.flask_app.app_context():
            response = self.client.get(url_for('single_bucket_list', id=89),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token})
            print(response.status_code)
            self.assertEqual(response.status_code, 204)

    def test_the_user_can_get_a_single_bucket_list(self):
        """ Test that the user can get a single bucket list """
        # create a bucket list
        payload = {"bucket_list_id": 100, "bucket_list_name": "sharon", "created_by": 10012}
        response = self.client.post("/v1/bucketlists", data=json.dumps(payload),
                                    headers={'Content-Type': 'application/json', 'Authorization': self.token})
        self.assertEqual(response.status_code, 201)

        # get the single bucket list
        with app.flask_app.app_context():
            response = self.client.get(url_for('single_bucket_list', id=100),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                       )
            self.assertEqual(response.status_code, 200)

    def test_the_user_can_delete_a_single_bucket_list(self):
        """ Test that the user can delete a single bucket list """
        # create a bucket list
        payload = {"bucket_list_id": 101, "bucket_list_name": "sharon", "created_by": 10012}
        self.client.post("/v1/bucketlists", data=json.dumps(payload),
                         headers={'Content-Type': 'application/json', 'Authorization': self.token})

        with app.flask_app.app_context():
            response = self.client.get(url_for('single_bucket_list', id=101),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                       )
            self.assertEqual(response.status_code, 200)


class TestItemResource(unittest.TestCase):
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        self.client.post("/v1/auth/register", data=json.dumps(payload), content_type='application/json')

        # get auth token
        payload = {"username": "sharonkaren@gmail.com", "password": "password"}
        token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
        self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']

    def test_if_the_user_can_create_a_bucket_list_item(self):
        """ Tests if the user can create a bucket list item """

        # create a bucket list
        payload = {"bucket_list_id": 103, "bucket_list_name": "sharon", "created_by": 10012}
        self.client.post("/v1/bucketlists", data=json.dumps(payload),
                         headers={'Content-Type': 'application/json', 'Authorization': self.token})

        item_payload = {"list_id": 90, "item_name": "Valentine's day", "completed": "True"}
        with app.flask_app.app_context():
            response = self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                        )
            self.assertEqual(response.status_code, 201)

        # try and enter the bucket list again
        with app.flask_app.app_context():
            response = self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                        )
            self.assertEqual(response.status_code, 401)

    def test_that_the_user_cannot_enter_a_bucket_list_item_with_no_existing_bucket_list(self):
        """ Test that the user can not enter a bucket list item for a non existing bucket list """
        item_payload = {"list_id": 900, "item_name": "Valentine's day", "completed": "True"}
        with app.flask_app.app_context():
            response = self.client.post(url_for('items', id=10), data=json.dumps(item_payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                        )
            self.assertEqual(response.status_code, 401)


class TestItemsUpdate(unittest.TestCase):
    def setUp(self):
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'
        app.db.session.close()
        app.db.create_all()
        self.client = app.flask_app.test_client()
        # create a user
        payload = {"first_name": "Sharon", "last_name": "Njihia",
                   "email": "sharonkaren@gmail.com", "password": "password"}
        self.client.post("/v1/auth/register", data=json.dumps(payload), content_type='application/json')

        # get auth token
        payload = {"username": "sharonkaren@gmail.com", "password": "password"}
        token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
        self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']

    def test_if_the_user_can_not_delete_a_bucket_list_item_that_does_not_exist(self):
        """ Test if the user can not delete a bucket list item that does not exist """
        with app.flask_app.app_context():
            response = self.client.delete(url_for('items_update', id=103, item_id=10),
                                          headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 401)















