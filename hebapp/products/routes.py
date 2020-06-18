from flask import Blueprint, jsonify
from hebapp.products.models import Product

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
def register():
    return jsonify({"message": "products"})