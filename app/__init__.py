from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    with app.app_context():
        from . import routes  # Importar as rotas dentro do contexto da aplicação
        db.create_all()

    return app
