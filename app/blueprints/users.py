from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db

MODELS_PATH = os.path.abspath(os.path.join(DB_PATH, '..'))
MODELS_PATH = os.path.abspath(os.path.join(MODELS_PATH, "app", "models"))
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
        sql = text("INSERT INTO Users (cpf_login, senha, email) VALUES (:cpf_login, :senha, :email) RETURNING user_id")
        dados = {"cpf_login": cpf_login, "senha": senha, "email": email}
    else:
        sql = text("INSERT INTO Users (cpf_login, senha, email, cndb) VALUES (:cpf_login, :senha, :email, :cndb) RETURNING user_id")
        dados = {"cpf_login": cpf_login, "senha": senha, "email": email, "cndb": cndb}

    result = db.session.execute(sql, dados)
    db.session.commit()

    id = result.fetchone()[0]
    dados['id'] = id

    return dados

# Logar
@users_bp.route("/login", methods = ["POST"])
def logar():
    cpf_login = reques.form.get("cpf")
    senha = request.form.get("senha")

    sql = text("SELECT cpf_login, senha FROM Users")

    try:
        result = db.session.execute(sql)
        linha = result.mappings().all()[1]
    
        return linha
    except Exception as e:
        return e

    if cpf_login in linha and senha in linha:
        return "Usuário logado com sucesso!"
    return "Usuário não existe"

# Criar tabelas
@users_bp.route("/criar")
def criar():
    create_all_tables()
    return "Todas as tabelas criadas com sucesso"
