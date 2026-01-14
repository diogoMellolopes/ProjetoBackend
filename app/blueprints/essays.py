from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity, jwt_required
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db, jwt

essays_bp = Blueprint('Essays', __name__, url_prefix = '/essays')

@essays_bp.route("/user_essay", methods=["POST"])
@jwt_required()
def postar():
    user_id = get_jwt_identity()

    titulo = request.form.get("titulo")
    tema = request.form.get("tema")
    redacao = request.form.get("redacao")

    if titulo == None or tema == None or redacao == None:
        return {"msg": "Insira todas as informações necessárias"}, 400

    if len(redacao) <= 50:
        return {"msg": "A redação precisa ter mais de 50 caracteres para ser considerada válida"}, 401

    sql = text("""INSERT INTO essays (titulo, tema, redacao, status, user_id)
                VALUES (:titulo, :tema, :redacao, :status, :user_id) RETURNING essay_id
                ON CONFLICT (titulo) DO NOTHING""")
    dados = {"titulo": titulo, "tema": tema, "redacao": redacao, "status": "pendente", "user_id": user_id}

    result = db.session.execute(sql, dados)
    db.session.commit()

    id = result.fetchone()[0]
    dados["id"] = id

    return jsonify(dados), 201

@essays_bp.route("/user_essay", methods=["GET"])
@jwt_required()
def pegar():
    user_id = get_jwt_identity()

    sql = text("""SELECT essay_id, titulo, tema, redacao, status, nota, avaliacao
                FROM essays WHERE user_id = :user_id""")
    dados = {"user_id": user_id}

    try:
        result = db.session.execute(sql, dados)
        relatorio = result.mappings().all()
        essays = [dict(row) for row in relatorio]

    except Exception as e:
        return e

    return jsonify(essays), 200

@essays_bp.route("/user_essay", methods=["DELETE"])
@jwt_required()
def deletar():
    user_id = get_jwt_identity()

    titulo = request.form.get("titulo")

    if titulo == None:
        return {"msg": "Insira o título da redação"}, 400

    sql = text("DELETE FROM essays WHERE user_id = :user_id AND titulo = :titulo RETURNING *")
    dados = {"user_id": user_id, "titulo": titulo}

    result = db.session.execute(sql, dados)
    db.session.commit()

    return {"msg": "Redação deletada com sucesso"}, 200

@essays_bp.route("/user_essay", methods=["PUT"])
@jwt_required()
def atualizar():
    user_id = get_jwt_identity()

    titulo = request.form.get("titulo")

    if titulo == None:
        return {"msg": "Insira o título da redação"}, 400

    sql = text("SELECT status FROM essays WHERE user_id = :user_id AND titulo = :titulo")
    dados = {"user_id": user_id, "titulo": titulo}

    try:
        result = db.session.execute(sql, dados)
        relatorio = result.mappings().all()
        essay = [dict(row) for row in relatorio]
    except Exception as e:
        return e

    if essay["status"] == "concluida":
        return {"msg": "Não pode alterar uma avaliação já avaliada"}, 400

    if tema == None or redacao == None:
        return {"msg": "Insira todas as informações necessárias"}, 400

    sql = text("""UPDATE essays SET 
                titulo = COALESCE(EXCLUDED.titulo, essays.titulo),
                tema = COALESCE(EXCLUDED.tema, essays.tema),
                redacao = COALESCE(EXCLUDED.redacao, essays.redacao)""")
    dados = {"titulo": titulo, "tema": tema, "redacao": redacao}

    result = db.session.execute(sql, dados)
    db.session.commit()

    return {"msg", "Redação atualizada com sucesso"}, 200