from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Categoria(db.Model):
    __tablename__ = "categorias"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(100))
    descricao: Mapped[str | None] = mapped_column(db.String(255))
    categoria_pai_id: Mapped[int | None] = mapped_column(db.ForeignKey("categorias.id"))
    ativo: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())