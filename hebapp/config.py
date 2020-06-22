from dotenv import load_dotenv
import os
load_dotenv()

class ProductionConfig():

    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig():

    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
