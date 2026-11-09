from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class Perfil(db.Model):
    __tablename__ = "perfis"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(30), unique=True)
    descricao: Mapped[str | None] = mapped_column(db.String(150))