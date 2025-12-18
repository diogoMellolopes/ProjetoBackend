from flask import Flask, Blueprint, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text 
from connect import db, init_db 
 
from blueprints.users import users_bp

app = Flask(__name__) 
init_db(app) 
  
app.register_blueprint(users_bp)
 
if __name__ == "__main__": 
    app.run(debug=True) 