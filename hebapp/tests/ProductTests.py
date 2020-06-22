import json
import sys
import os
topdir = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(topdir)
from hebapp import create_app, db
from hebapp.config import TestConfig
import unittest
from dotenv import load_dotenv
from hebapp.products.models import Product
from hebapp.units.models import Unit
from hebapp.departments.models import Department
from unittest.mock import patch
load_dotenv(verbose=False)

class ProductTests(unittest.TestCase):

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
    def test_create_product_success(self, mock_jwt_required):
        """
        Test that a product can be created
        """
        department = Department(name="produce")
        unit = Unit(name="each")
        with self.app.app_context():
            db.session.add(department)
            db.session.add(unit)
            db.session.commit()
        product = {
            "description": "cottage chese", 
            "last_sold": "2017-09-04",
            "shelf_life_days": 20,
            "department_id": 1,
            "unit_id": 1,
            "qty_sold_in": 1,
            "sell_price": 2.50,
            "cost_expense": 1.00}
        response = self.client.post(self.url_prefix + '/products', json=product)
        self.assertEqual(response.status_code, 201)
    
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    def test_create_product_fail_missing_field(self, mock_jwt_required):
        """
        Test that product schema catches a missing property
        """
        # no need to create mock department or unit for this scenario
        product = {
            "description": "cottage chese", 
            "last_sold": "2017-09-04",
            "shelf_life_days": 20,
            "department_id": 1,
            "unit_id": 1,
            "qty_sold_in": 1,
            "cost_expense": 1.00}
        # missing 'sell_price'
        response = self.client.post(self.url_prefix + '/products', json=product)
        self.assertEqual(response.status_code, 400)

    def test_create_product_fail_missing_auth(self):
        """
        Test that a product can't be created without a token
        """
        product = {
            "description": "cottage chese", 
            "last_sold": "2017-09-04",
            "shelf_life_days": 20,
            "department_id": 1,
            "unit_id": 1,
            "qty_sold_in": 1,
            "cost_expense": 1.00}
        response = self.client.post(self.url_prefix + '/products', json=product)
        self.assertEqual(response.status_code, 401)
        
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    """
    additional tests to do:
    1. invalid length for fields in registration POST
    """
    

if __name__ == '__main__':
    unittest.main()