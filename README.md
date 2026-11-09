# Sistema de Chamados de TI

Aplicação web para centralizar solicitações de suporte técnico: colaboradores abrem e acompanham chamados, o administrador distribui as demandas e os técnicos atendem, com controle de prazos, histórico completo e acesso restrito por perfil.

**Versão da documentação:** 2.0 · **Status:** especificação fechada, implementação não iniciada.

## Stack

Python · Flask (Blueprints) · Jinja2 (HTML) · Tailwind CSS · JavaScript · PostgreSQL · SQLAlchemy · Flask-Migrate / Login / WTF · Docker Compose · Git/GitHub.

## Índice da documentação

| Documento | Conteúdo |
|---|---|
| [REQUISITOS.md](/docs/REQUISITOS.md) | Objetivo, escopo, perfis, requisitos funcionais e não funcionais, MVP x Fase 2 |
| [REGRAS_DE_NEGOCIO.md](/docs/REGRAS_DE_NEGOCIO.md) | Prazos, expediente, estados, retenção de anexos, notificações |
| [PERMISSOES.md](/docs/PERMISSOES.md) | Matriz de acesso por perfil e política de segurança |
| [FLUXOS.md](/docs/FLUXOS.md) | Diagramas: ciclo de vida, atribuição, cadastro, senha, anexos |
| [BANCO_DE_DADOS.md](/docs/BANCO_DE_DADOS.md) | Modelo de dados (18 tabelas) e regras de integridade |
| [banco.dbml](/docs/banco.dbml) | Modelo para colar no dbdiagram.io |
| [ARQUITETURA.md](/docs/ARQUITETURA.md) | Camadas, estrutura de pastas, execução em Linux/Windows |

## Fases

- **MVP (Fase 1):** autenticação e cadastro, chamados, atribuição e transferência, mensagens, notas internas, anexos, prazos em horas úteis, notificações no sistema, dashboard, administração de usuários, categorias e configurações.
- **Fase 2:** notificações por e-mail, alertas automáticos de prazo, retenção automática de anexos, base de conhecimento e recorrência de chamados.

## Histórico de versões

| Versão | Mudança |
|---|---|
| 1.0 | Levantamento inicial (`DOCUMENTACAO.md`) |
| 2.0 | Requisitos renumerados e corrigidos; regras de prazo e retenção definidas; matriz de permissões; arquitetura Flask + Jinja; modelo de dados ampliado de 12 para 18 tabelas |