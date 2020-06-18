from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv


load_dotenv(verbose=False)

DB_URL = os.getenv("DATABASE_URL")

# initialize the application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# intialize the database
db = SQLAlchemy(app)

# intitialize marshmallow
ma = Marshmallow(app)

# from hebitems import routes


from hebapp.users.routes import users
from hebapp.items.routes import items

app.register_blueprint(users)
app.register_blueprint(items)