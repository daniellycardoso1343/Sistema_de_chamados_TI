from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401

    @app.get("/health")
    def health():
        return {"status": "ok"}
    
    @app.get("/teste")
    def teste():
        return render_template("teste.html")
    
    return app