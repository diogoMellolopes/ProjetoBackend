from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity, jwt_required
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db, jwt

MEDIA_CORTE = {
    "medicina": 810,
    "ciencia_da_computacao": 760,
    "direito": 710,
    "medicina_veterinaria": 720,
    "administracao": 570,
    "biblioteconomia": 660,
    "lingua_estrangeira": 580,
    "letras": 620,
    "engenharia": 720
}

dashboards_bp = Blueprint('Dashboards', __name__, url_prefix = '/dashboards')

@dashboards_bp.route("/stats", methods=["GET"])
@jwt_required()
def ver_estatisticas():
    user_id = get_jwt_identity()

    sql = ( """SELECT avg(nota) FROM essays WHERE user_id = :user_id AND nota > 0""")
    dados = {"user_id": user_id}

    result = db.session.execute(sql, dados)
    media = dict(result.mappings().fetchone())

    sql = ("""SELECT nota FROM essays WHERE user_id = :user_id LIMIT 1
           ORDER BY data DESC""")
    dados = {"user_id": user_id}

    result = db.session.execute(sql, dados)
    ultima_nota = dict(result.mappings().fetchone())

    if len(media) == 0 or len(ultima_nota):
        return "Você ainda não tem redações avaliadas", 404

    sql = ("""SELECT curso_desejado FROM profiles WHERE user_id = :user_id""")
    dados = {"user_id": user_id}

    return jsonify(media), jsonify(ultima_nota), 200

@dashboards_bp.route("/stats/<metric>", methods=["GET"])
@jwt_required()
def consultar(metric):
    user_id = get_jwt_identity()
    
    sql = ("""""")