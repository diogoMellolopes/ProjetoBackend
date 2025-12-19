import sys, os
from sqlalchemy import text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(DB_PATH)
from connect import db

def create_user():
    sql = text("""CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY, 
    cpf_login VARCHAR(11) NOT NULL UNIQUE, 
    senha VARCHAR NOT NULL, 
    email VARCHAR(50) NOT NULL, 
    cndb INT
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Criado tabela usuários com sucesso")

def create_profile():
    sql = text("""CREATE TABLE IF NOT EXISTS Profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    foto_perfil BYTEA,
    curso_desejado VARCHAR(50),
    universidade_desejada VARCHAR(50),
    uf VARCHAR(2),
    cidade VARCHAR(29),
    nome VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Criado tabela perfis com sucessos")

def create_essays():
    sql = text("""CREATE TABLE IF NOT EXISTS Essays (
    essay_id BIGSERIAL PRIMARY KEY,
    tema VARCHAR(50) NOT NULL,
    redacao VARCHAR NOT NULL,
    nota VARCHAR,
    status BOOLEAN NOT NULL,
    user_id INT NOT NULL,
    avaliacao VARCHAR,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Craida tabela redações com sucesso")

def create_all_tables():
    create_user()
    create_profile()
    create_essays()