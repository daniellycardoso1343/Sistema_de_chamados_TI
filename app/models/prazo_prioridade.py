from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class PrazoPrioridade(db.Model):
    __tablename__ = "prazos_prioridade"
    __table_args__ = (
        db.CheckConstraint("prioridade IN ('baixa', 'media', 'alta')", name="ck_prazos_prioridade_prioridade"),
    )
    
    prioridade: Mapped[str] = mapped_column(db.String(20), primary_key=True)
    minutos_atribuicao: Mapped[int] = mapped_column(db.Integer)
    minutos_resolucao: Mapped[int] = mapped_column(db.Integer)
    atualizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True), onupdate=db.func.now())