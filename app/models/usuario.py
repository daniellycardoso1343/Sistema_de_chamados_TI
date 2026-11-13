from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(100))
    email: Mapped[str] = mapped_column(db.String(150), unique=True)
    senha_hash: Mapped[str] = mapped_column(db.String(255))
    perfil_id: Mapped[int] = mapped_column(db.ForeignKey("perfis.id"))
    setor: Mapped[str | None] = mapped_column(db.String(100))
    ativo: Mapped[bool] = mapped_column(default=False)
    email_confirmado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    ultimo_login_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    bloqueado_ate: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())
    atualizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True), onupdate=db.func.now())
    tentativas_falhas: Mapped[int] = mapped_column(default=0)