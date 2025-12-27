from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db, jwt

profiles_bp = Blueprint('Profiles', __name__, url_prefix = '/profiles')

@profiles_bp.route("/update", methods = ["PUT"])
@jwt_required()
def atualizar():
    user_id = get_jwt_identity()

    curso_desejado = request.form.get("curso_desejado")
    universidade_desejada = request.form.get("universidade_desejada")
    uf = request.form.get("uf")
    cidade = request.form.get("cidade")
    nome = request.form.get("nome")
    foto = request.files.get("foto")

    foto_byte = foto.read() if foto else None

    if uf != None and len(uf) != 2:
        return {"msg": "UF deve ter exatemente duas linhas"}, 400

    sql = text("""INSERT INTO profiles (user_id, nome, curso_desejado, universidade_desejada, cidade, uf, foto_perfil)
               VALUES (:user_id, :nome, :curso_desejado, :universidade_desejada, :cidade, :uf, :foto_perfil)
               ON CONFLICT (user_id)
               DO UPDATE SET 
               nome = COALESCE(EXCLUDED.nome, profiles.nome), 
               curso_desejado = COALESCE(EXCLUDED.curso_desejado, profiles.curso_desejado), 
               universidade_desejada = COALESCE(EXCLUDED.universidade_desejada, profiles.universidade_desejada), 
               cidade = COALESCE(EXCLUDED.cidade, profiles.cidade), 
               uf = COALESCE(EXCLUDED.uf, profiles.uf),
               foto_perfil = COALESCE(EXCLUDED.foto_perfil, profiles.foto_perfil)""")
    
    dados = {"user_id": user_id, "curso_desejado": curso_desejado, "universidade_desejada": universidade_desejada, 
             "uf": uf, "cidade": cidade, "foto_perfil": foto_byte, "nome": nome}

    result = db.session.execute(sql, dados)
    db.session.commit()

    return {"msg": "Perfil atualizado com sucesso"}, 200