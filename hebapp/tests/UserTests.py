import json
import sys
import os
topdir = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(topdir)
from hebapp import create_app, db
from hebapp.config import TestConfig
import unittest
from dotenv import load_dotenv
from hebapp.users.models import User
load_dotenv(verbose=False)

class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.url_prefix = prefix = os.getenv("URL_PREFIX")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_model_create(self):
        """
        Makes sure the User model will save
        """
        with self.app.app_context():
            user = User(first_name="sam", email="testone@gmail.com", password="password")
            users = None
            db.session.add(user)
            db.session.commit()
            users = User.query.all()
            self.assertEqual(len(users), 1)

    # why to use json attribute https://stackoverflow.com/a/54945825/7858114
    def test_register_success(self):
        """
        Makes sure the registration route works in a happy path
        """
        user = {"first_name": "sam", "email": "testtwo@gmail.com", "password":"password"}
        response = self.client.post(self.url_prefix + '/register', json=user)
        self.assertEqual(response.status_code, 201)
    
    def test_register_fail_missing_field(self):
        """
        Makes sure the registration route works in a happy path
        """
        user = {"email": "testtwo@gmail.com", "password":"password"}
        response = self.client.post(self.url_prefix + '/register', json=user)
        self.assertEqual(response.status_code, 400)
    
    def test_login_success(self):
        """
        Makes sure the login route works in a happy path
        """
        user = {"first_name": "sam", "email": "testtwo@gmail.com", "password":"password"}
        self.client.post(self.url_prefix + '/register', json=user)
        response = self.client.post(self.url_prefix + '/login', json={"email": "testtwo@gmail.com", "password": "password"})
        self.assertEqual(response.status_code, 200)

    def test_login_fail_bad_password(self):
        """
        Makes sure the login route returns 401 when a bad password is given
        """
        user = {"first_name": "sam", "email": "testtwo@gmail.com", "password":"password"}
        self.client.post(self.url_prefix + '/register', json=user)
        response = self.client.post(self.url_prefix + '/login', json={"email": "testtwo@gmail.com", "password": "mypassword"})
        self.assertEqual(response.status_code, 401)

    def test_create_existing_user(self):
        """
        Makes sure the registration route blocks duplicate emails
        """
        user = {"first_name": "sam", "email": "testtwo@gmail.com", "password":"password"}
        self.client.post(self.url_prefix + '/register', json=user)
        response = self.client.post(self.url_prefix + '/register', json=user)
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_dict.get('message').lower(), 'User already exists for this email'.lower())

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    """
    additional tests to do:
    1. invalid length for fields in registration POST
    """
    

if __name__ == '__main__':
    unittest.main()