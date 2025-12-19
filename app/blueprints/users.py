from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db
from connect_bcrypt import bcrypt

MODELS_PATH = os.path.abspath(os.path.join(DB_PATH, '..'))
MODELS_PATH = os.path.abspath(os.path.join(MODELS_PATH, "app", "models"))
sys.path.append(MODELS_PATH)
from create_tabels import create_all_tables

users_bp = Blueprint('Users', __name__, url_prefix = '/users')

@users_bp.route("/register", methods = ["POST"])
def registrar():
    criar_tabelas()

    cpf_login = request.form.get("cpf")

    for i in cpf_login:
        try:
            int(i)
        except ValueError:
            return "O CPF deve ser composto apenas dos números"

    senha = request.form.get("senha")
    senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    email = request.form.get("email")

    cndb = request.form.get("cndb", None)

    if cndb == None:
        sql = text("INSERT INTO Users (cpf_login, senha, email) VALUES (:cpf_login, :senha_hash, :email) RETURNING user_id")
        dados = {"cpf_login": cpf_login, "senha_hash": senha_hash, "email": email}
    else:
        sql = text("INSERT INTO Users (cpf_login, senha, email, cndb) VALUES (:cpf_login, :senha_hash, :email, :cndb) RETURNING user_id")
        dados = {"cpf_login": cpf_login, "senha_hash": senha_hash, "email": email, "cndb": cndb}

    result = db.session.execute(sql, dados)
    db.session.commit()

    id = result.fetchone()[0]
    dados['id'] = id

    return dados

@users_bp.route("/login", methods = ["POST"])
def logar():
    cpf_login = request.form.get("cpf")
    senha = request.form.get("senha")

    sql = text("SELECT cpf_login, senha FROM Users")

    try:
        result = db.session.execute(sql)
        linha = result.mappings().all()[1]
    
        return linha
    except Exception as e:
        return e

    if cpf_login in linha:
        return "Usuário logado com sucesso!"
    return "Usuário não existe"

def criar_tabelas():
    create_all_tables()