from flask import Blueprint, jsonify
from hebapp import db
from hebapp.users.models import User, UserJwt, UserSchema
from hebapp.users.utils import serialize_many

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
def register():
    return jsonify({"message": "register"})

@users.route("/users", methods=['GET'])
def get():
    users = User.query.all()
    users = serialize_many(users)
    return jsonify(users)
