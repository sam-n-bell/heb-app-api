from flask import Blueprint, jsonify, request, Response, abort
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from hebapp.utils import return_marshmallow_schema_errors
from hebapp.units.models import UnitSchema, Unit
from hebapp import db
from hebapp.units.utils import serialize_many

units = Blueprint('units', __name__)

@units.route('/units', methods=['GET'])
@jwt_required
def get_units():
    all_units = Unit.query.all()
    all_units = serialize_many(all_units)
    return jsonify(all_units)