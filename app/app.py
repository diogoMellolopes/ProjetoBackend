from flask import Flask, Blueprint, request, jsonify 
from sqlalchemy import text 
from connect import init_db, init_bcrypt, init_jwt

from blueprints.users import users_bp
from blueprints.profiles import profiles_bp
from blueprints.essays import essays_bp

app = Flask(__name__) 
init_db(app) 
init_bcrypt(app)
init_jwt(app)

app.register_blueprint(users_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(essays_bp)

if __name__ == "__main__": 
    app.run(debug=True) 