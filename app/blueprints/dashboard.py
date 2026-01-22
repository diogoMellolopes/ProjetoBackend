from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity, jwt_required
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db, jwt

dashboards_bp = Blueprint('Dashboards', __name__, url_prefix = '/dashboards')

@dashbaords_bp.route("/stats", methods=["GET"])
@jwt_required()
def ver_estatisticas():
    user_id = get_jwt_identity()

    sql = ("""SELECT avg(nota), nota FROM essays WHERE user_id = :user_id""")
    dados = {"user_id": user_id}