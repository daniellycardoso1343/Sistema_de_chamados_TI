from flask import Flask
from app.config import Config
from app.extensions import db, migrate 
from app.models.perfil import Perfil
from app.models.usuario import Usuario
from app.models.configuracao import Configuracao
from app.models.categoria import Categoria
from app.models.chamado import Chamado
from app.models.prazo_prioridade import PrazoPrioridade


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        return{"Status": "ok"}
    
    from app import models
    return app  