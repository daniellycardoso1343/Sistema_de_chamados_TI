from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class DominioAutorizado(db.Model):
    __tablename__ = "dominios_autorizados"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    dominio: Mapped[str] = mapped_column(db.String(150), unique=True)
    ativo: Mapped[bool] = mapped_column(db.Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())