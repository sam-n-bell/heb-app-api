from flask import Blueprint, jsonify, request, Response, abort
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from hebapp.utils import return_marshmallow_schema_errors
from hebapp.departments.models import Department, DepartmentSchema
from hebapp import db
from hebapp.departments.utils import serialize_many

departments = Blueprint('departments', __name__)

@departments.route('/departments', methods=['GET'])
@jwt_required
def get_departments():
    depts = Department.query.all()
    depts = serialize_many(depts)
    return jsonify(depts)