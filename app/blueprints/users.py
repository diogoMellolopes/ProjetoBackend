from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.connect import db, bcrypt

users_bp = Blueprint('Users', __name__, url_prefix = '/users')

@users_bp.route("/register", methods = ["POST"])
def registrar():
    cpf_login = request.form.get("cpf")
    senha = request.form.get("senha")
    email = request.form.get("email")

    if cpf_login == None or senha == None or email == None:
        return {"msg": "Insira todos os dados necessários"}, 400

    if len(cpf_login) != 11 or not cpf_login.isdigit():
        return {"msg": "O CPF inválido"}, 400
        
    senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    cndb = request.form.get("cndb", None)

    sql = text("""INSERT INTO users (cpf_login, senha, email, cndb, data_de_criacao) 
                VALUES (:cpf_login, :senha_hash, :email, :cndb, CURRENT_DATE) RETURNING user_id""")
    dados = {"cpf_login": cpf_login, "senha_hash": senha_hash, "email": email, "cndb": cndb}

    try:
        result = db.session.execute(sql, dados)
        user_id = result.fetchone()[0]
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"msg": "CPF já cadastrado no banco"}, 400

    return jsonify({"msg": "Usuário criado com sucesso", "user_id": user_id}), 201

@users_bp.route("/login", methods = ["POST"])
def logar():
    cpf_login = request.form.get("cpf")
    senha = request.form.get("senha")

    if cpf_login == None or senha == None:
        return {"msg": "Por favor insira os dados necessários"}, 400

    sql = text("SELECT user_id, cpf_login, senha FROM Users WHERE cpf_login = :cpf_login")
    dados = {"cpf_login": cpf_login}

    result = db.session.execute(sql, dados)
    user = result.mappings().first()

    if user == None:
        return {"msg": "Usuário não encontrado"}, 404
    
    senha_hash = user["senha"]
    if bcrypt.check_password_hash(senha_hash, senha):
        acess_token = create_access_token(identity = str(user["user_id"]))
        return jsonify(acess_token = acess_token), 200
    
    return {"msg": "Senha incorreta"}, 401
    
@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protegido():
    user = get_jwt_identity()
    return jsonify(logged_in_as = user), 200    