from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv


load_dotenv(verbose=False)

DB_URL = os.getenv("DATABASE_URL")

# initialize the application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# intialize the database
db = SQLAlchemy(app)

# intitialize marshmallow
ma = Marshmallow(app)

jwt_secret = os.getenv("JWT_SECRET")
app.config['JWT_SECRET_KEY'] = jwt_secret

# class UserTwo(db.Model):
#     __tablename__ = 'userstwo'
#     user_id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     first_name = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.Text, nullable=False)

# db.create_all()

from hebapp.units.models import Unit
from hebapp.departments.models import Department
from hebapp.users.routes import users
from hebapp.products.routes import products

app.register_blueprint(users)
app.register_blueprint(products)

@app.errorhandler(400)
def bad_request(e):
    return jsonify(message=e.description), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(message=e.description), 401

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(message=e.description), 404

@app.errorhandler(500)
def internal_system_error(e):
    return jsonify(message=e.description), 500