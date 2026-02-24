from sqlalchemy import text
from app.connect import db

def create_user():
    sql = text("""CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY, 
    cpf_login VARCHAR(11) NOT NULL UNIQUE, 
    senha TEXT NOT NULL, 
    email VARCHAR(100) NOT NULL, 
    cndb TEXT,
    data_de_criacao DATE
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Criado tabela usuários com sucesso")

def create_profile():
    sql = text("""CREATE TABLE IF NOT EXISTS Profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    foto_perfil BYTEA,
    curso_desejado VARCHAR(100),
    universidade_desejada VARCHAR(100),
    uf VARCHAR(2),
    cidade VARCHAR(50),
    nome VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Criado tabela perfis com sucessos")

def create_essays():
    sql = text("""CREATE TABLE IF NOT EXISTS Essays (
    essay_id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    tema VARCHAR(100) NOT NULL,
    redacao TEXT NOT NULL,
    nota INT,
    status BOOLEAN NOT NULL,
    user_id INT NOT NULL,
    avaliacao TEXT,
    data DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )""")

    result = db.session.execute(sql)
    db.session.commit()

    return print("Criada tabela redações com sucesso")

def create_courses():
    sql = text("""CREATE TABLE IF NOT EXISTS Courses (
    course_id SERIAL PRIMARY KEY,
    nome_curso VARCHAR(100) UNIQUE NOT NULL,
    nota_curso INT NOT NULL
    )""")

    result = db.session.execute(sql)
    db.session.commit()

def populate_courses():
    sql = text("""
    INSERT INTO Courses (nome_curso, nota_curso)
    VALUES
        ('medicina', 810),
        ('ciencia_da_computacao', 760),
        ('direito', 710),
        ('medicina_veterinaria', 720),
        ('administracao', 570),
        ('biblioteconomia', 660),
        ('lingua_estrangeira', 580),
        ('letras', 620),
        ('pedagogia', 650),
        ('matematica', 680),
        ('historia', 590)
    ON CONFLICT (nome_curso) DO NOTHING
    """)
    db.session.execute(sql)
    db.session.commit()
    print("Cursos populados com sucesso.")

def create_all_tables():
    create_courses()
    populate_courses()
    create_user()
    create_profile()
    create_essays()