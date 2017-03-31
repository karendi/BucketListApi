import json
import os
import unittest
from flask import url_for
from app import flask_app, db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseTestCase(unittest.TestCase):
    """ setting up the test database"""
    def setUp(self):
        flask_app.config.from_object('flask_settings.config_default.TestingConfig')
        flask_app.config['SERVER_NAME'] = '127.0.0.0'
        db.session.close()
        db.create_all()
        self.client = flask_app.test_client()

        with flask_app.app_context():
            # create a user
            payload = {"first_name": "Sharon", "last_name": "Njihia",
                       "email": "sharonkaren@gmail.com", "password": "password"}
            self.client.post(url_for('user_registration'), data=json.dumps(payload),
                             content_type='application/json')
            # get auth token
            payload = {"username": "sharonkaren@gmail.com", "password": "password"}
            token = self.client.post("/auth", data=json.dumps(payload), content_type='application/json')
            self.token = 'JWT ' + json.loads(token.get_data(as_text=True))['access_token']


class TestRegistration(unittest.TestCase):
    def setUp(self):
        """ setting up the test database """
        flask_app.config.from_object('flask_settings.config_default.TestingConfig')
        db.session.close()
        db.drop_all()
        db.create_all()
        self.client = flask_app.test_client()

    def test_user_registration(self):
        """ Tests that checks if a user is able to register successfully"""
        with flask_app.app_context():
            # create a user
            payload = {"first_name": "Sharon", "last_name": "Njihia",
                       "email": "sharonkaren@gmail.com", "password": "password"}
            response = self.client.post(url_for('user_registration'), data=json.dumps(payload),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)

    def test_the_user_payload_being_sent(self):
        """ Tests that the payload with user data has all the required info"""
        with flask_app.app_context():
            # create a user
            payload = {}
            response = self.client.post(url_for('user_registration'), data=json.dumps(payload),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_the_user_exists(self):
        """ Tests that when a user exists , they are not registered again"""
        with flask_app.app_context():
            # register the person
            payload = {"first_name": "Sharon", "last_name": "Njihia",
                       "email": "sharonkaren@gmail.com", "password": "password"}
            self.client.post(url_for('user_registration'), data=json.dumps(payload),
                             content_type='application/json')
            # try and register the user again
            payload = {"first_name": "Sharon", "last_name": "Njihia",
                       "email": "sharonkaren@gmail.com", "password": "password"}
            response = self.client.post(url_for('user_registration'), data=json.dumps(payload),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 401)

    def tearDown(self):
        db.session.remove()


class TestBucketList(BaseTestCase):
    def test_if_user_can_create_bucket_list(self):
        """ Test if a user can create a bucket list"""
        # create a bucket list
        with flask_app.app_context():
            payload = {"bucket_list_id": 89, "bucket_list_name": "sharon", "created_by": 10012}
            response = self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 201)

    def test_if_user_can_get_bucket_lists(self):
        """ Test if a user can get bucket lists """
        with flask_app.app_context():
            response = self.client.get(url_for('get_and_post_bucket_list', limit=1, page=1),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 200)

    def test_if_the_user_can_filter_bucket_lists(self):
        """ Test if the user can filter the bucket list results """
        with flask_app.app_context():
            response = self.client.get(url_for('get_and_post_bucket_list', limit=1, page=1, q='xys'),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 200)


class TestSingleBucketList(BaseTestCase):
    def test_if_the_user_cant_get_a_bucket_list_if_it_does_not_exist(self):
        """ Test if the user can not get a single bucket list if it does not exist """
        with flask_app.app_context():
            response = self.client.get(url_for('single_bucket_list', id=89),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token})
            print(response.status_code)
            self.assertEqual(response.status_code, 404)

    def test_the_user_can_get_a_single_bucket_list(self):
        """ Test that the user can get a single bucket list """
        with flask_app.app_context():
            # create a bucket list
            payload = {"bucket_list_id": 100, "bucket_list_name": "sharon", "created_by": 10012}
            self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})
            # get the single bucket list
            response = self.client.get(url_for('single_bucket_list', id=100),
                                       headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                       )
            self.assertEqual(response.status_code, 200)

    def test_the_user_can_delete_a_single_bucket_list(self):
        """ Test that the user can delete a single bucket list """
        with flask_app.app_context():

            # create a bucket list
            payload = {"bucket_list_id": 101, "bucket_list_name": "sharon", "created_by": 10012}
            self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})
            response = self.client.delete(url_for('single_bucket_list', id=101),
                                          headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 200)

    def test_the_user_cannot_delete_a_single_bucket_list_that_does_not_exist(self):
        """ Test that the user can not delete a single bucket list that does not exist """
        with flask_app.app_context():
            # delete the bucket list
            response = self.client.delete(url_for('single_bucket_list', id=200),
                                          headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 404)


class TestItemResource(BaseTestCase):
    def test_if_the_user_can_create_a_bucket_list_item(self):
        """ Tests if the user can create a bucket list item """

        with flask_app.app_context():
            # create a bucket list
            payload = {"bucket_list_id": 103, "bucket_list_name": "sharon", "created_by": 10012}
            self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})
            # create a bucket list item
            item_payload = {"list_id": 90, "item_name": "Valentine's day", "completed": "True"}
            self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})
            # try and enter the bucket list again
            response = self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                        )
            self.assertEqual(response.status_code, 401)

    def test_that_the_user_cannot_enter_a_bucket_list_item_with_no_existing_bucket_list(self):
        """ Test that the user can not enter a bucket list item for a non existing bucket list """
        item_payload = {"list_id": 900, "item_name": "Valentine's day", "completed": "True"}
        with flask_app.app_context():
            response = self.client.post(url_for('items', id=10), data=json.dumps(item_payload),
                                        headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                        )
            self.assertEqual(response.status_code, 401)


class TestItemsUpdate(BaseTestCase):
    def test_if_the_user_can_not_delete_a_bucket_list_item_that_does_not_exist(self):
        """ Test if the user can not delete a bucket list item that does not exist """
        with flask_app.app_context():
            response = self.client.delete(url_for('items_update', id=103, item_id=10),
                                          headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 401)

    def test_the_user_can_delete_a_bucket_list_item(self):
        """ Test that the user can delete a bucket list item """
        with flask_app.app_context():
            # create a bucket list
            payload = {"bucket_list_id": 103, "bucket_list_name": "sharon", "created_by": 10012}
            self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})

            # create a bucket_list_item
            item_payload = {"list_id": 190, "item_name": "Valentine's day", "completed": "True"}
            self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})

            # delete the bucket list item
            response = self.client.delete(url_for('items_update', id=103, item_id=190),
                                          headers={'Content-Type': 'application/json', 'Authorization': self.token})
            self.assertEqual(response.status_code, 200)

    def test_if_the_user_can_update_a_bucket_list_item(self):
        """ Test if the user can update a bucket list item"""
        with flask_app.app_context():
            # create a bucket list
            payload = {"bucket_list_id": 103, "bucket_list_name": "sharon", "created_by": 10012}
            self.client.post(url_for('get_and_post_bucket_list'), data=json.dumps(payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})

            # create the bucket list item
            item_payload = {"list_id": 90, "item_name": "Valentine's day", "completed": "True"}
            self.client.post(url_for('items', id=103), data=json.dumps(item_payload),
                             headers={'Content-Type': 'application/json', 'Authorization': self.token})
            # edit the bucket list item
            update_item_payload = {"item_name": "XYZ", "completed": "False"}
            list_response = self.client.put(url_for('items_update', id=103, item_id=90),
                                            data=json.dumps(update_item_payload),
                                            headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                            )
            self.assertEqual(list_response.status_code, 200)

    def test_the_user_can_not_update_a_bucket_list_item_that_does_not_exist(self):
        """ Test the user can not update a bucket list item that does not exist """
        with flask_app.app_context():
            update_item_payload = {"item_name": "XYZ", "completed": "False"}
            list_response = self.client.put(url_for('items_update', id=789, item_id=90),
                                            data=json.dumps(update_item_payload),
                                            headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                            )
            self.assertEqual(list_response.status_code, 401)

    def test_the_user_can_not_update_with_an_empty_payload(self):
        """ Test that the user cannot update with an empty payload"""
        with flask_app.app_context():
            update_item_payload = {}
            list_response = self.client.put(url_for('items_update', id=789, item_id=90),
                                            data=json.dumps(update_item_payload),
                                            headers={'Content-Type': 'application/json', 'Authorization': self.token}
                                            )
            self.assertEqual(list_response.status_code, 400) 