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

    sql = text("""SELECT avg(nota) as media FROM essays WHERE user_id = :user_id AND nota > 0""")
    dados = {"user_id": user_id}

    result = db.session.execute(sql, dados)
    relatorio = result.mappings().fetchone()
    media = relatorio["media"] if relatorio else None

    sql = text("""SELECT nota FROM essays WHERE user_id = :user_id AND nota > 0
           ORDER BY data DESC LIMIT 1""")
    dados = {"user_id": user_id}

    result = db.session.execute(sql, dados)
    relatorio = result.mappings().fetchone()
    ultima_nota = relatorio["nota"] if relatorio else None

    if media == None or ultima_nota == None:
        return {"msg": "Você ainda não tem redações avaliadas"}, 404

    sql = text("""SELECT curso_desejado FROM profiles WHERE user_id = :user_id""")
    dados = {"user_id": user_id}

    result = db.session.execute(sql, dados)
    relatorio = result.mappings().fetchone()
    curso_desejado = relatorio["curso_desejado"] if relatorio else None

    if curso_desejado != None:
        curso_desejado = normalizar_nome(curso_desejado)
        if curso_desejado.lower() in MEDIA_CORTE.keys() and ultima_nota >= MEDIA_CORTE[curso_desejado.lower()]:
            return {"msg": f"Você passaria com sua nota em {curso_desejado}", "media": media, "ultima_nota": ultima_nota}, 200
        else:
            return {"msg": f"Você não passaria com sua nota em {curso_desejado}", "media": media, "ultima_nota": ultima_nota}, 200

    return {"msg": f"Não foi possivel encontrar o seu curso desejado: {curso_desejado}", "media": media, "ultima_nota": ultima_nota}, 404

COLUNAS_VALIDAS = {
    "uf": "profiles.uf",
    "city": "profiles.cidade",
    "target_course": "profiles.curso_desejado",
    "target_uni": "profiles.universidade_desejada",
    "tema": "essays.tema"
}

@dashboards_bp.route("/stats/<metric>/<metric_value>/<int:page>", methods=["GET"])
@jwt_required()
def consultar(metric, metric_value, page):
    if metric not in COLUNAS_VALIDAS:
        return {"msg": "Métrica inválida"}, 400
    
    if page < 0:
        return {"msg": "Selecione uma página válida"}, 404
    
    order = request.args.get("order", "desc").upper()
    order = "DESC" if order != "ASC" else "ASC"
    
    page = page * 10
    
    coluna = COLUNAS_VALIDAS[metric]
    
    sql = text(f"""SELECT profiles.nome, profiles.user_id, essays.nota FROM profiles
           JOIN essays on profiles.user_id = essays.user_id
           WHERE {coluna} = :metric_value AND essays.nota IS NOT NULL
           ORDER BY essays.nota {order}
           LIMIT 10 OFFSET :page""")
    dados = {"metric_value": metric_value, "page": page}

    result = db.session.execute(sql, dados)
    relatorio = result.mappings().all()
    resultado = [dict(row) for row in relatorio]

    if len(relatorio) == 0:
        return {"msg": "Não há dados suficientes para essa pesquisa"}, 404
    
    return jsonify(resultado), 200

def normalizar_nome(nome):
    return nome.lower().replace(" ", "_")