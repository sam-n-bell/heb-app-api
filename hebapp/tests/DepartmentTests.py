import json
import sys
import os
topdir = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(topdir)
from hebapp import create_app, db
from hebapp.config import TestConfig
import unittest
from hebapp.departments.models import Department
from unittest.mock import patch
from dotenv import load_dotenv
load_dotenv(verbose=False)

class DepartmentTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.url_prefix = prefix = os.getenv("URL_PREFIX")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    # why patch is needed: https://stackoverflow.com/a/57612953/7858114
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    def test_get_departments_success(self, mock_jwt_required):
        """
        Test that a department is returned from GET departments
        """
        with self.app.app_context():
            department = Department(name="produce")
            db.session.add(department)
            db.session.commit()
        response = self.client.get(self.url_prefix + '/departments')
        depts = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(depts), 1)
    
    def test_get_departments_requires_auth(self):
        """
        Test that  GET departments requires auth
        """
        response = self.client.get(self.url_prefix + '/departments')
        self.assertEqual(response.status_code, 401)


    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    

if __name__ == '__main__':
    unittest.main()