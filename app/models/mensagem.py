from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Mensagem(db.Model):
    __tablename__ = "mensagens"
    __table_args__ = (
        db.Index("ix_mensagens_chamado_criado", "chamado_id", "criado_em"),
    )  
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"))
    autor_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    conteudo: Mapped[str] = mapped_column(db.Text)
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())
    