from flask import Blueprint, jsonify, request, Response
from hebapp.products.models import Product
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from hebapp.utils import return_marshmallow_schema_errors
from hebapp.products.models import ProductModelSchema
from hebapp import db

product_model_schema = ProductModelSchema()

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
def register():
    return jsonify({"message": "products"})

@products.route('/products', methods=['POST'])
@jwt_required
def create_product():
    product_request = request.json
    errors = product_model_schema.validate(product_request)
    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))
    
    product = Product(description=product_request.get('description'),
                        last_sold=product_request.get('last_sold'),
                        shelf_life=product_request.get('shelf_life'),
                        department_id=product_request.get('department_id'),
                        sell_price=product_request.get('sell_price'),
                        unit_id=product_request.get('unit_id'),
                        qty_sold_in=product_request.get('qty_sold_in'),
                        cost_expense=product_request.get('cost_expense'))

    db.session.add(product)
    db.session.commit()
    return Response(None, 201)