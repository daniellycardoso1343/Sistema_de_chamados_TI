# Arquitetura do Sistema

## 1. Visão geral

Aplicação web monolítica em Flask, que renderiza páginas HTML no servidor (Jinja2) e usa JavaScript apenas onde a interação exige. Um único projeto, um único deploy, organizado em módulos.

## 2. Tecnologias

| Camada | Tecnologia | Papel |
|---|---|---|
| Linguagem | Python 3.12+ | Backend |
| Framework | Flask + Blueprints | Rotas e módulos |
| Páginas | Jinja2 (HTML) | Templates com herança, includes e macros |
| Estilo | Tailwind CSS (CLI) | Visual e responsividade |
| Interação | JavaScript (opcional: Alpine.js) | Modais, filtros e menus |
| Banco | PostgreSQL | Dados relacionais |
| ORM | SQLAlchemy via Flask-SQLAlchemy | Acesso ao banco |
| Migrations | Flask-Migrate (Alembic) | Versionamento do esquema |
| Sessão | Flask-Login | Usuário autenticado |
| Formulários | Flask-WTF | Validação e CSRF |
| E-mail | Flask-Mail | Confirmação, recuperação e notificações |
| Tarefas | APScheduler em processo separado (Fase 2) | Alertas e retenção de anexos |
| Arquivos | `filetype` | Detecção do tipo real do arquivo, em Linux e Windows |
| Servidor | waitress | Funciona em Linux e Windows |
| Contêineres | Docker Compose | App, PostgreSQL, worker, servidor de e-mail de teste |
| Testes | pytest | Regras de permissão e de prazo |
| Versão | Git e GitHub | Código e documentação |

## 3. Camadas

```text
Navegador
   │ HTTP
   ▼
routes.py     recebe a requisição, valida o formulário, chama o service, devolve a página
   ▼
services.py   regras de negócio, permissões, transações e histórico
   ▼
models/       entidades SQLAlchemy
   ▼
PostgreSQL
```

| Camada | Pode | Não pode |
|---|---|---|
| `routes` | Ler a requisição, chamar services, renderizar templates | Conter regra de negócio ou consultar o banco |
| `services` | Aplicar regras, consultar e gravar via models, controlar a transação | Conhecer `request` ou HTML |
| `models` | Definir colunas, relacionamentos e restrições | Conter fluxo de negócio |
| `utils` | Funções compartilhadas (permissões, prazos, e-mail, arquivos) | Depender de um módulo específico |

Não há camada de repositories: o SQLAlchemy já cumpre esse papel.

## 4. Estrutura de pastas

```text
sistema-chamados-ti/
├── run.py                       ponto de entrada (desenvolvimento)
├── worker.py                    processo de tarefas agendadas (Fase 2)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── package.json                 Tailwind CLI
├── .env.example
├── .gitignore
├── README.md
│
├── app/
│   ├── __init__.py              create_app()
│   ├── config.py
│   ├── extensions.py            db, migrate, login_manager, csrf, mail
│   ├── cli.py                   flask seed, criar-admin, seed-demo
│   ├── errors.py                páginas 403, 404, 500
│   ├── jobs.py                  tarefas agendadas
│   │
│   ├── models/                  um arquivo por tabela (18)
│   ├── utils/                   permissions.py, prazos.py, email.py, arquivos.py
│   │
│   ├── auth/                    login, cadastro, confirmação, recuperação
│   ├── usuarios/                gestão de contas (admin) e perfil próprio
│   ├── chamados/                abrir, listar, detalhar, status, conclusão, cancelamento
│   ├── categorias/              administração de categorias
│   ├── atribuicoes/             atribuir e transferir
│   ├── mensagens/               mensagens e notas internas
│   ├── anexos/                  upload, download, preservação
│   ├── notificacoes/            central de notificações
│   ├── configuracoes/           prazos, expediente, domínios, limites
│   ├── solucoes/                base de conhecimento (Fase 2)
│   ├── dashboard/               indicadores
│   │       (cada módulo: __init__.py, routes.py, services.py, forms.py)
│   │
│   ├── templates/               base.html, partials/, macros, uma pasta por módulo, emails/, errors/
│   └── static/                  css/input.css, css/output.css, js/, img/
│
├── instance/                    fora do Git
│   └── uploads/                 anexos
│
├── migrations/
├── tests/                       conftest.py, test_permissoes.py, test_prazos.py, test_chamados.py
└── docs/
```

## 5. Responsabilidades dos módulos

| Módulo | Responsabilidade |
|---|---|
| `auth` | Login, logout, cadastro, confirmação de e-mail, recuperação de senha, bloqueio por falhas |
| `usuarios` | CRUD de contas, ativação, perfil, "meu perfil" |
| `chamados` | Ciclo do chamado, filtros, status, previsão, conclusão e cancelamento |
| `categorias` | CRUD com ativação |
| `atribuicoes` | Atribuir, transferir, validar a regra do solicitante |
| `mensagens` | Mensagens e notas internas |
| `anexos` | Upload validado, download autorizado, preservação |
| `notificacoes` | Criar e listar notificações, marcar como lidas |
| `configuracoes` | Prazos, expediente, domínios e limites |
| `solucoes` | Base de conhecimento com busca (Fase 2) |
| `dashboard` | Indicadores por perfil |

## 6. Fluxo de uma requisição

1. O navegador envia a requisição; o Flask encontra a rota.
2. O decorator confere login e perfil.
3. O formulário (Flask-WTF) valida os dados e o token CSRF.
4. O service aplica permissões e regras, grava dados, histórico e notificações em **uma transação**.
5. A rota devolve a página renderizada ou redireciona.
6. Em caso de erro, o service lança uma exceção de negócio e a rota mostra uma mensagem amigável; erros inesperados vão para o log e a página 500 genérica.

## 7. Prazos em horas úteis

O módulo `utils/prazos.py` concentra o cálculo (início do expediente, fim, dias úteis lidos de `configuracoes`) e expõe funções como `somar_minutos_uteis(inicio, minutos)` e `minutos_uteis_entre(a, b)`. É código puro, sem acesso ao banco, o que permite testar com os exemplos de REGRAS_DE_NEGOCIO.md.

## 8. Tarefas agendadas (Fase 2)

Um processo separado (`worker.py`) executa com APScheduler: lembretes de prazo, exclusão de anexos não preservados, envio de e-mails pendentes. Fica separado do servidor web para não duplicar tarefas quando houver vários processos. Funciona igual em Linux e Windows. No MVP, "próximo do vencimento" e "vencido" são calculados na hora da consulta, sem worker.

## 9. Execução em Linux e Windows

| Item | Decisão |
|---|---|
| Desenvolvimento | Nativo nos dois sistemas: `python -m venv`, `pip install -r requirements.txt`, `flask run` |
| Caminhos | Sempre `pathlib` / `os.path.join`; nunca barras fixas |
| Servidor | `waitress-serve` (Linux e Windows) |
| Banco e e-mail | Docker Compose: PostgreSQL e um servidor de e-mail de teste |
| Tailwind | `npx tailwindcss` (Node.js), igual nos dois |
| Finais de linha | `.gitattributes` com `* text=auto` |

Serviços do `docker-compose.yml`: `db` (PostgreSQL), `app` (waitress), `worker` (Fase 2) e `mailpit` (caixa de e-mail de desenvolvimento).

## 10. Configuração

Variáveis em `.env`, lidas por `config.py`: `SECRET_KEY`, `DATABASE_URL`, `MAIL_*`, `FLASK_ENV`. Em produção, a aplicação recusa iniciar com chave padrão ou sem banco configurado. Regras que o administrador altera (prazos, expediente, limites, domínios) ficam no banco, não no `.env`.

## 11. Logs e erros

- Log da aplicação em arquivo com rotação, sem dados sensíveis (nunca senha, token ou conteúdo de chamado).
- Eventos de segurança em `log_seguranca`.
- Páginas 403, 404 e 500 sem detalhes técnicos.

## 12. Testes

- **Permissões:** para cada linha da matriz de PERMISSOES.md, um teste de acesso permitido e um de acesso negado.
- **Prazos:** os exemplos validados de REGRAS_DE_NEGOCIO.md, mais bordas (fim de expediente, fim de semana).
- **Fluxos:** abertura, atribuição, transferência, conclusão, cancelamento.
- **Segurança:** acesso por ID alheio devolve 404, autocadastro com perfil forjado é ignorado, upload inválido é recusado.
- Banco de teste isolado, criado a cada execução.

## 13. Convenções

- Nomes de arquivos, tabelas e funções em português, sem acentos; classes em `PascalCase` singular (`Chamado`).
- Commits descritivos, uma funcionalidade por commit; ramo `main` estável e ramos por funcionalidade.
- Migrations sempre versionadas no Git.

## 14. Fases de implementação

| Etapa | Entrega |
|---|---|
| 1 | Base visual (Tailwind, `base.html`, partials, macros) |
| 2 | Banco: models, migration e seed |
| 3 | Autenticação, cadastro e permissões |
| 4 | Núcleo dos chamados |
| 5 | Atribuição, mensagens, notas e anexos |
| 6 | Prazos em horas úteis e notificações no sistema |
| 7 | Dashboard e administração (usuários, categorias, configurações) |
| 8 | Testes, revisão de segurança e Docker |
| 9 | Fase 2: e-mails, worker, retenção de anexos, base de conhecimento, recorrência |