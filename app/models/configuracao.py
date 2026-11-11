from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Configuracao(db.Model):
    __tablename__ = "configuracoes"

    chave: Mapped[str] = mapped_column(db.String(60), primary_key=True)
    valor: Mapped[str] = mapped_column(db.String(255))
    descricao: Mapped[str | None] = mapped_column(db.String(255))
    atualizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True), onupdate=db.func.now())
    