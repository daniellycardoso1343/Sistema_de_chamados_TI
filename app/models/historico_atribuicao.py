from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class HistoricoAtribuicao(db.Model):
    __tablename__ = "historico_atribuicoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"))
    tecnico_anterior_id: Mapped[int | None] = mapped_column(db.ForeignKey("usuarios.id"))
    tecnico_novo_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    administrador_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    justificativa: Mapped[str | None] = mapped_column(db.Text)
    atribuido_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())