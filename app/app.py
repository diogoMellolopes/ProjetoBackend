from flask import Flask
from app.connect import init_db, init_bcrypt, init_jwt
from app.models import create_tabels
from app.blueprints.users import users_bp
from app.blueprints.profiles import profiles_bp
from app.blueprints.essays import essays_bp
from app.blueprints.dashboard import dashboards_bp

app = Flask(__name__) 
init_db(app) 
init_bcrypt(app)
init_jwt(app)

app.register_blueprint(users_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(essays_bp)
app.register_blueprint(dashboards_bp)

try:
    with app.app_context():
        create_tabels.create_all_tables()
except Exception as e:
    print("Erro ao criar tabelas:", e)