from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime

class Solucao(db.Model):
    __tablename__ = "solucoes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(db.String(150))
    descricao_problema: Mapped[str] = mapped_column(db.Text)
    passo_a_passo: Mapped[str] = mapped_column(db.Text)
    categoria_id: Mapped[int | None] = mapped_column(db.ForeignKey("categorias.id"))
    chamado_origem_id: Mapped[int | None] = mapped_column(db.ForeignKey("chamados.id"))
    autor_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    ativo: Mapped[bool] = mapped_column(db.Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())
    atualizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True), onupdate=db.func.now())
    