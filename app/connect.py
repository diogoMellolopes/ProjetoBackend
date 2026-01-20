from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()

def init_bcrypt(app):
    bcrypt.init_app(app)

db = SQLAlchemy()

def init_db(app):
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/student_core_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

jwt = JWTManager()

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = "bolo"
    jwt.init_app(app)