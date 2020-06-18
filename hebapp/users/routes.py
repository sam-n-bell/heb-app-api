from flask import Blueprint, jsonify, abort, Response, request
from flask_bcrypt import Bcrypt
from hebapp import db, app
from hebapp.users.models import User, UserJwt, UserSchema, LoginSchema
from hebapp.users.utils import serialize_many, return_marshmallow_schema_errors
from sqlalchemy import func
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

secret = os.getenv("jwt_secret")

users = Blueprint('users', __name__)

login_schema = LoginSchema()

bcrypt = Bcrypt(app)

@users.route('/register', methods=['POST'])
def register():
    login = request.json
    errors = login_schema.validate(login)
    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))

    existing = User.query.filter(func.lower(User.email) == login.get('email').lower()).one_or_none()
    if existing is not None:
        abort(400, description="User already exists for this email")
    
    login['password'] = bcrypt.generate_password_hash(login.get('password'), 10)
    new_user = User(email=login.get('email'), password=login.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return Response(None, 201)

@users.route("/users", methods=['GET'])
def get():
    users = User.query.all()
    users = serialize_many(users)
    return jsonify(users)
