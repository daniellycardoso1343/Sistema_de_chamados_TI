from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class HistoricoPrioridade(db.Model):
    __tablename__ = "historico_prioridades"
    __table_args__ = (
        db.CheckConstraint(
            "prioridade_anterior IN ('baixa', 'media', 'alta')",
            name="ck_historico_prioridades_prioridade_anterior",
        ),
        db.CheckConstraint(
            "prioridade_nova IN ('baixa', 'media', 'alta')",
            name="ck_historico_prioridades_prioridade_nova"
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"))
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    prioridade_anterior: Mapped[str] = mapped_column(db.String(50))
    prioridade_nova: Mapped[str] = mapped_column(db.String(20))
    justificativa: Mapped[str] = mapped_column(db.Text)
    alterado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())