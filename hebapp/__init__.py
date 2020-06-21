from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv(verbose=False)

DB_URL = os.getenv("DATABASE_URL")

# initialize the application
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# intialize the database
db = SQLAlchemy(app)



# intitialize marshmallow
ma = Marshmallow(app)

jwt_secret = os.getenv("JWT_SECRET")
app.config['JWT_SECRET_KEY'] = jwt_secret

from hebapp.units.models import Unit
from hebapp.departments.models import Department
from hebapp.users.routes import users
from hebapp.products.routes import products
from hebapp.units.routes import units
from hebapp.departments.routes import departments

prefix = os.getenv("URL_PREFIX")
app.register_blueprint(users, url_prefix=prefix)
app.register_blueprint(products, url_prefix=prefix)
app.register_blueprint(units, url_prefix=prefix)
app.register_blueprint(departments, url_prefix=prefix)

@app.route('/', methods=['GET'])
def index():
    return Response("API for H-E-B coding exercise. By Sam Bell."), 200

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