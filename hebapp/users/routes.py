from flask import Blueprint, jsonify, abort, Response, request, current_app
from hebapp import db, bcrypt, jwt
from hebapp.users.models import User, UserJwt, UserSchema, RegistrationSchema, LoginSchema
from hebapp.users.utils import serialize_many, serialize_one
from hebapp.utils import return_marshmallow_schema_errors
from sqlalchemy import func
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

users = Blueprint('users', __name__)

registration_schema = RegistrationSchema()
login_schema = LoginSchema()

@users.route('/register', methods=['POST'])
def register():
    login = request.json
    # validate that the json body contains good data
    errors = registration_schema.validate(login)
    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))

    # check that the email is not already in use
    existing = User.query.filter(func.lower(User.email) == login.get('email').lower()).one_or_none()
    if existing is not None:
        abort(400, description="User already exists for this email")
    
    # hash the user password for security sake
    # Why using .decode() => https://stackoverflow.com/a/38262440/7858114
    login['password'] = bcrypt.generate_password_hash(login.get('password'), 10).decode('utf8')
    new_user = User(email=login.get('email'), password=login.get('password'), first_name=login.get('first_name'))
    db.session.add(new_user)
    db.session.commit()
    return Response(None, 201)

@users.route('/login', methods=['POST'])
def login():
    login = request.json
    # validate that the json body contains good data
    errors = login_schema.validate(login)
    if errors:
        abort(400, description=return_marshmallow_schema_errors(errors))

    # make sure email exists and password matches
    user = User.query.filter(func.lower(User.email) == login.get('email').lower()).one_or_none()
    if user is None:
        abort(401, description="No account registered for this email")
    elif not bcrypt.check_password_hash(user.password, login.get('password')):
        abort(401, description="Invalid Login Credentials")

    # create jwt token
    access_token = create_access_token(identity=serialize_one(user), expires_delta=timedelta(days=1))
    user_jwt = UserJwt(jwt=access_token, user_id=user.user_id)
    db.session.add(user_jwt)
    db.session.commit()
    return Response(access_token, 200)