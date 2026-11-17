from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class LogSeguranca(db.Model):
    __tablename__ = 'log_seguranca'
    __table_args__ = (
    db.Index("ix_log_seguranca_evento_criado", "evento", "criado_em"),
)
    
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(db.ForeignKey("usuarios.id"), index=True)
    evento: Mapped[str] = mapped_column(db.String(50))
    ip: Mapped[str | None] = mapped_column(db.String(45))
    detalhes: Mapped[str | None] = mapped_column(db.Text)
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())