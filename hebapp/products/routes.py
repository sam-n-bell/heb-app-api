from flask import Blueprint, jsonify, request, Response
from hebapp.products.models import Product
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from hebapp.utils import return_marshmallow_schema_errors
from hebapp.products.models import ProductModelSchema, ProductView
from hebapp import db
from hebapp.products.utils import serialize_many

product_model_schema = ProductModelSchema()

products = Blueprint('products', __name__)

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

@products.route('/products', methods=['GET'])
@jwt_required
def search_products():
    description = request.args.get('description')
    sold_from = request.args.get('soldFrom')
    sold_to = request.args.get('soldTo')
    sold_on = request.args.get('soldOn')
    min_life = request.args.get('minLife')
    max_life = request.args.get('maxLife')
    exact_life = request.args.get('exactLife')
    department = request.args.get('department')
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')
    selling_unit = request.args.get('sellUnit')
    min_cost = request.args.get('minCost')
    max_cost = request.args.get('maxCost')
    sell_count = request.args.get('soldInCounts')


    filters = []
    if department:
        filters.append(ProductView.department == department)
    if description:
        filters.append(ProductView.description.like('%'+description+'%'))
    if sold_from:
        filters.append(ProductView.last_sold >= sold_from)
    if sold_to:
        filters.append(ProductView.last_sold <= sold_to)
    if sold_on:
        filters.append(ProductView.last_sold == sold_on)
    if min_price:
        filters.append(ProductView.sell_price >= min_price)
    if max_price:
        filters.append(ProductView.sell_price <= max_price)
    if min_cost:
        filters.append(ProductView.cost_expense >= min_cost)
    if max_cost:
        filters.append(ProductView.cost_expense <= max_cost)
    if min_life:
        filters.append(ProductView.shelf_life >= min_life)
    if max_life:
        filters.append(ProductView.shelf_life <= max_life)
    if exact_life:
        filters.append(ProductView.shelf_life == exact_life)
    if selling_unit:
        filters.append(ProductView.unit == selling_unit)
    if sell_count:
        filters.append(ProductView.qty_sold_in == sell_count)

    # filters = tuple(filters)
    product_views = ProductView.query.filter(*tuple(filters)).all()
    product_views = serialize_many(product_views)
    return jsonify(product_views)