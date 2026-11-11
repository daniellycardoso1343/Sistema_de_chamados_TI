from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class TokenUsuario(db.Model):
    __tablename__ = "tokens_usuario"
    __table_args__ = (
        db.CheckConstraint("finalidade IN ('confirmar_email', 'redefinir_senha')", name="ck_tokens_usuario_finalidade"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    token_hash: Mapped[str] = mapped_column(db.String(255), unique=True)
    finalidade: Mapped[str] = mapped_column(db.String(30))
    expira_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True))
    utilizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())