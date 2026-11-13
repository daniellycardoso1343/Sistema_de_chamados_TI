from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class HistoricoStatus(db.Model):
    __tablename__ = "historico_status"
    __table_args__ = (
        db.CheckConstraint(
            "status_anterior IN ('aberto', 'em_atendimento', 'concluido', 'cancelado')",
            name="ck_historico_status_status_anterior",
        ),
        db.CheckConstraint(
            "status_novo IN ('aberto', 'em_atendimento', 'concluido', 'cancelado')",
            name="ck_historico_status_status_novo",
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"))
    status_anterior: Mapped[str | None] = mapped_column(db.String(50))
    status_novo: Mapped[str] = mapped_column(db.String(30))
    justificativa: Mapped[str | None] = mapped_column(db.Text)
    alterado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))