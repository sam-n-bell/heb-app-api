from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
from flask_cors import CORS
from hebapp.config import ProductionConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

load_dotenv(verbose=False)

# intialize the database
db = SQLAlchemy()

# intitialize marshmallow
ma = Marshmallow()

bcrypt = Bcrypt()

jwt = JWTManager()

from hebapp.units.models import Unit
from hebapp.departments.models import Department
from hebapp.users.routes import users
from hebapp.products.routes import products
from hebapp.units.routes import units
from hebapp.departments.routes import departments

def create_app(config_class=ProductionConfig):
    # initialize the application
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(ProductionConfig)
    prefix = os.getenv("URL_PREFIX")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

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

    return app