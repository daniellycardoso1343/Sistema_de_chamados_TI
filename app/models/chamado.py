from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime


class Chamado(db.Model):
    __tablename__ = "chamados"
    __table_args__ = (
        db.CheckConstraint("status IN ('aberto', 'em_atendimento', 'concluido', 'cancelado')", name="ck_chamados_status"),
        db.CheckConstraint("prioridade IN ('baixa', 'media', 'alta')", name="ck_chamados_prioridade"),
        db.CheckConstraint("prioridade_solicitada IN ('baixa', 'media', 'alta')", name="ck_chamados_prioridade_solicitada"),
        db.CheckConstraint("previsao_conclusao IS NULL OR limite_resolucao IS NULL OR previsao_conclusao <= limite_resolucao", name="ck_chamados_previsao"),
        db.CheckConstraint("tec_responsavel_id IS NULL OR tec_responsavel_id <> solicitante_id", name="ck_chamados_tecnico_solicitante"),
        db.CheckConstraint("status <> 'concluido' OR solucao_aplicada IS NOT NULL", name="ck_chamados_concluido_solucao"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(db.String(20), unique=True)
    solicitante_id: Mapped[int] = mapped_column(db.ForeignKey("usuarios.id"))
    tec_responsavel_id: Mapped[int | None] = mapped_column(db.ForeignKey("usuarios.id"))
    categoria_id: Mapped[int] = mapped_column(db.ForeignKey("categorias.id"))
    titulo: Mapped[str] = mapped_column(db.String(250))
    descricao: Mapped[str] = mapped_column(db.Text)
    prioridade_solicitada: Mapped[str] = mapped_column(db.String(20))
    prioridade: Mapped[str] = mapped_column(db.String(20))
    status: Mapped[str] = mapped_column(db.String(30), default="aberto")
    solucao_aplicada: Mapped[str | None] = mapped_column(db.Text)
    prazo_atribuicao: Mapped[datetime] = mapped_column(db.DateTime(timezone=True))
    atribuido_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    limite_resolucao: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    previsao_conclusao: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    anexos_decisao_solicitada_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    anexos_decisao_concluida_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    atualizado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True), onupdate=db.func.now())
    encerrado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    cancelado_em: Mapped[datetime | None] = mapped_column(db.DateTime(timezone=True))
    chamado_relacionado_id: Mapped[int | None] = mapped_column(db.ForeignKey("chamados.id"))
    criado_em: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=db.func.now())