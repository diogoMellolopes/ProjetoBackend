from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = ("postgresql://postgres:garototo@localhost:5432/student_core_db")

    db.init_app(app)