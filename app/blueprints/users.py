from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db, bcrypt, jwt

MODELS_PATH = os.path.abspath(os.path.join(DB_PATH, '..'))
MODELS_PATH = os.path.abspath(os.path.join(MODELS_PATH, "app", "models"))
sys.path.append(MODELS_PATH)
from create_tabels import create_all_tables

users_bp = Blueprint('Users', __name__, url_prefix = '/users')

@users_bp.route("/register", methods = ["POST"])
def registrar():
    criar_tabelas()

    cpf_login = request.form.get("cpf")
    senha = request.form.get("senha")
    email = request.form.get("email")

    if cpf_login == None or senha == None or email == None:
        return "Por favor insira todas as informações necessárias para o cadastro"

    for i in cpf_login:
        try:
            int(i)
        except:
            return "O CPF deve ser composto apenas dos números"
        
    senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    cndb = request.form.get("cndb", None)

    if cndb == None:
        sql = text("INSERT INTO users (cpf_login, senha, email) VALUES (:cpf_login, :senha_hash, :email) RETURNING user_id")
        dados = {"cpf_login": cpf_login, "senha_hash": senha_hash, "email": email}
    else:
        sql = text("INSERT INTO users (cpf_login, senha, email, cndb) VALUES (:cpf_login, :senha_hash, :email, :cndb) RETURNING user_id")
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

    if cpf_login == None or senha == None:
        return "Por favor insira CPF e Senha"

    sql = text("SELECT user_id, cpf_login, senha FROM Users WHERE cpf_login = :cpf_login")
    dados = {"cpf_login": cpf_login}

    try:
        result = db.session.execute(sql, dados)
        user = result.mappings().first()

    except Exception as e:
        return e

    if user == None:
        return "Usuário não existe"

    senha_hash = user["senha"]
    if bcrypt.check_password_hash(senha_hash, senha):
        acess_token = create_access_token(identity = user["user_id"])
        return jsonify(acess_token = acess_token)
    
    return "Senha está incorreta"
    
@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protegido():
    user = get_jwt_identity()
    return jsonify(logged_in_as = user)

def criar_tabelas():
    create_all_tables()