from flask import Blueprint, jsonify, abort, Response, request
from flask_bcrypt import Bcrypt
from hebapp import db, app
from hebapp.users.models import User, UserJwt, UserSchema, RegistrationSchema, LoginSchema
from hebapp.users.utils import serialize_many, return_marshmallow_schema_errors, serialize_one
from sqlalchemy import func
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv(verbose=True)

secret = os.getenv("jwt_secret")

users = Blueprint('users', __name__)

registration_schema = RegistrationSchema()
login_schema = LoginSchema()

bcrypt = Bcrypt(app)

jwt = JWTManager(app)


@users.route('/register', methods=['POST'])
def register():
    login = request.json
    errors = registration_schema.validate(login)
    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))

    existing = User.query.filter(func.lower(User.email) == login.get('email').lower()).one_or_none()
    if existing is not None:
        abort(400, description="User already exists for this email")
    
    # Why using .decode() => https://stackoverflow.com/a/38262440/7858114
    login['password'] = bcrypt.generate_password_hash(login.get('password'), 10).decode('utf8')
    new_user = User(email=login.get('email'), password=login.get('password'), first_name=login.get('first_name'))
    db.session.add(new_user)
    db.session.commit()
    return Response(None, 201)

@users.route('/login', methods=['POST'])
def login():
    login = request.json
    errors = login_schema.validate(login)

    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))

    user = User.query.filter(func.lower(User.email) == login.get('email').lower()).one_or_none()
    if user is None:
        abort(401, description="No account registered for this email")
    elif not bcrypt.check_password_hash(user.password, login.get('password')):
        abort(401, description="Invalid Login Credentials")

    access_token = create_access_token(identity=serialize_one(user), expires_delta=timedelta(days=1))
    user_jwt = UserJwt(jwt=access_token, user_id=user.user_id)
    db.session.add(user_jwt)
    db.session.commit()
    return Response(access_token, 200)

@users.route("/users", methods=['GET'])
def get():
    users = User.query.all()
    users = serialize_many(users)
    return jsonify(users)
