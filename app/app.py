from flask import Flask, Blueprint, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text 
from connect import db, init_db
from flask_bcrypt import Bcrypt

from blueprints.users import users_bp
from connect_bcrypt import init_bcrypt

app = Flask(__name__) 
init_db(app) 
init_bcrypt(app)



app.register_blueprint(users_bp)
 
if __name__ == "__main__": 
    app.run(debug=True) 