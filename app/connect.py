from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()

def init_bcrypt(app):
    bcrypt.init_app(app)

def init_db(app):
    database_url = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

def init_jwt(app):
    jwt_secret = os.getenv("JWT_SECRET_KEY")

    app.config["JWT_SECRET_KEY"] = jwt_secret
    jwt.init_app(app)