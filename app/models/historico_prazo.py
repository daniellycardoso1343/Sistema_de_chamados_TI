from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class HistoricoPrazo(db.Model):
    __tablename__ = "historico_prazos"
    __table_args__ = (
        db.CheckConstraint(
            "tipo_prazo IN ('atribuicao', 'limite_resolucao', 'previsao')",
            name="ck_historico_prazo_tipo_prazo",
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"))
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    tipo_prazo: Mapped[str] = mapped_column(db.String(20))
    prazo_anterior: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    prazo_novo: Mapped[datetime] = mapped_column(db.DateTime(timezone=True))
    justificativa: Mapped[str | None] = mapped_column(db.Text)
    alterado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now()) 