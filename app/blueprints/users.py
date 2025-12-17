from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db

MODELS_PATH = os.path.abspath(os.path.join(DB_PATH, '..'))
sys.path.append(MODELS_PATH)
from create_tabels import *

users_bp = Blueprint('Users', __name__, url_prefix = '/users')

# Cadastrar
@users_bp.route("/register", methods = ["POST"])
def registrar():
    create_user()

    cpf_login = request.form.get("cpf")
    senha = request.form.get("senha")
    email = request.form.get("email")

    try:
        cndb = request.form.get("cnd")
    except Exception as e:
        cndb = None
        print(f"erro: {e}")

    if cndb == None:
        sql = text("INSERT INTO Users (cpf_login, senha, email) VALUES (:cpf_login, :senha, :email) RETURNING ID")
        dados = {"cpf_login": cpf_login, "senha": senha, "email": email}
    else:
        sql = text("INSERT INTO Users (cpf_login, senha, email, cndb) VALUES (:cpf_login, :senha, :email, :cndb) RETURNING ID")
        dados = {"cpf_login": cpf_login, "senha": senha, "email": email, "cndb": cndb}

    result = db.session.execute(sql, dados)
    db.session.commit()

    id = result.fetchone()[0]
    dados['id'] = id

    return dados

@users_bp.route("/login", methods = ["POST"])
def logar():
    cpf_login = reques.form.get("cpf")
    senha = request.form.get("senha")