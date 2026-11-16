from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Notificacao(db.Model):
     __tablename__ = "notificacoes"
     __table_args__ = (
         db.CheckConstraint(
             "tipo IN ('chamado_aberto', 'chamado_atribuido', 'chamado_transferido','nova_mensagem','status_alterado','prioridade_alterada','prazo_proximo','prazo_vencido','selecao_anexos')",
             name="ck_notificacao_tipo"
         ),
         db.Index("ix_notificacoes_usuario_lida", "usuario_id", "lida_em"),
     )

     id: Mapped[int] = mapped_column(primary_key=True)
     usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
     chamado_id: Mapped[int | None] = mapped_column(db.ForeignKey("chamados.id"))
     tipo: Mapped[str] = mapped_column(db.String(50))
     titulo: Mapped[str] = mapped_column(db.String(150))
     mensagem: Mapped[str | None] = mapped_column(db.String(500))
     lida_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
     email_enviado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
     criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())
    