import sys, os
from sqlalchemy import text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db

def create_user():
    sql = text("""CREATE TABLE IT NOT EXISTS Users (userID SERIAL PRIMARY KEY, cpf_login INT NOT NULL UNIQUE, 
    senha VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL, 
    target_course VARCHAR(50), target_uni VARCHAR(50), cndb INT)""")
    result = db.session.execute(sql)
    db.session.commit()

    return print("Criado tabela usuários com sucesso")