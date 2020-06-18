from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
load_dotenv(verbose=False)

DB_URL = os.getenv("DATABASE_URL")

# initialize the application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://otjwcedrzwqkkm:e02351da2e46b3df7074ee87dde211dcd9be105ab07ce8c4efa4b1dadf7b1411@ec2-52-44-166-58.compute-1.amazonaws.com:5432/d3tfvp71nifho5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# intialize the database
db = SQLAlchemy(app)

# intitialize marshmallow
ma = Marshmallow(app)

@app.route('/test', methods=['GET'])
def test_app():
    return jsonify({"message": "hello"})


if __name__ == '__main__':
    app.run(debug=True)
