from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from connect import db, init_db

app = Flask(__name__)
init_db(app)

@app.route("/")
def teste():
    try:
        teste = text("SELECT 1")
        db.session.execute(teste)
        return "Funcionionando"
    except Exception as e:
        return f"Erro: {e}"

if __name__ == "__main__":
    app.run(debug=True)

"""from flask import Flask
from conf.database import init_db

from control.marca import marca_bp
from control.produto import produto_bp

app = Flask(__name__)

init_db(app)

app.register_blueprint(marca_bp)
app.register_blueprint(produto_bp)

if __name__ == "__main__":
    app.run(debug=True)"""