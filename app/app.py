from flask import Flask
from connect import init_db, init_bcrypt, init_jwt
from models import create_tabels

from blueprints.users import users_bp
from blueprints.profiles import profiles_bp
from blueprints.essays import essays_bp
from blueprints.dashboard import dashboards_bp

app = Flask(__name__) 
init_db(app) 
init_bcrypt(app)
init_jwt(app)

app.register_blueprint(users_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(essays_bp)
app.register_blueprint(dashboards_bp)

if __name__ == "__main__": 
    with app.app_context():
        create_tabels.create_all_tables()

    app.run(debug=True) 