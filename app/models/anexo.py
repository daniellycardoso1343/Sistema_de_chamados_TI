from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Anexo(db.Model):
    __tablename__ = "anexos"

    id: Mapped[int] = mapped_column(primary_key=True)
    chamado_id: Mapped[int] = mapped_column(db.ForeignKey("chamados.id"), index=True)
    mensagem_id: Mapped[int | None] = mapped_column(db.ForeignKey("mensagens.id"))
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    nome_original: Mapped[str] = mapped_column(db.String(255))
    nome_armazenado: Mapped[str] = mapped_column(db.String(255), unique=True)
    caminho_arquivo: Mapped[str] = mapped_column(db.String(500))
    tipo_arquivo: Mapped[str] = mapped_column(db.String(100))
    tamanho_bytes: Mapped[int] = mapped_column(db.BigInteger)
    hash_sha256: Mapped[str | None] = mapped_column(db.String(64))
    preservado: Mapped[bool] = mapped_column(db.Boolean, default=False)
    excluido_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())