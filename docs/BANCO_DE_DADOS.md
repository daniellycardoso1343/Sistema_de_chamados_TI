# Banco de Dados

## 1. Tecnologia

PostgreSQL, modelado em DBML ([banco.dbml](banco.dbml)) e visualizado no dbdiagram.io. As tabelas são criadas e versionadas por **migrations** (Flask-Migrate/Alembic), nunca por SQL manual no ambiente.

## 2. Tabelas (18)

### Acesso e contas
| Tabela | Finalidade |
|---|---|
| `perfis` | Os três níveis de acesso: colaborador, tecnico, admin |
| `usuarios` | Contas, com controle de bloqueio por falhas de login |
| `tokens_usuario` | Tokens (em hash) de confirmação de e-mail e redefinição de senha |
| `dominios_autorizados` | Domínios de e-mail permitidos no autocadastro |

### Chamados
| Tabela | Finalidade |
|---|---|
| `categorias` | Categorias e subcategorias (auto-relacionamento) |
| `chamados` | Solicitações de suporte, com os três prazos |
| `mensagens` | Conversa entre solicitante e TI (imutável) |
| `notas_internas` | Observações privadas da equipe de TI |
| `anexos` | Metadados dos arquivos (o arquivo fica no disco) |

### Histórico
| Tabela | Finalidade |
|---|---|
| `historico_status` | Mudanças de status |
| `historico_prioridades` | Mudanças de prioridade |
| `historico_atribuicoes` | Atribuições e transferências |
| `historico_prazos` | Alterações de prazo, previsão e extensão de limite |

### Apoio
| Tabela | Finalidade |
|---|---|
| `prazos_prioridade` | Prazos de atribuição e resolução por prioridade, em minutos úteis |
| `configuracoes` | Expediente, limites de anexo, retenção, bloqueio de login |
| `notificacoes` | Notificações dentro do sistema |
| `solucoes` | Base de conhecimento (Fase 2) |
| `log_seguranca` | Auditoria de login e de acessos negados |


## 4. Integridade

**Restrições de valor** (aplicadas como enums ou `CHECK` no banco):
- `status` ∈ {aberto, em_atendimento, concluido, cancelado}; `prioridade` ∈ {baixa, media, alta}.
- `previsao_conclusao <= limite_resolucao`.
- `tec_responsavel_id <> solicitante_id` (ninguém atende o próprio chamado).
- `status = concluido` exige `solucao_aplicada`.

**Exclusão:** nada é apagado fisicamente. Usuários e categorias são desativados (`ativo = false`). Chaves estrangeiras usam `ON DELETE RESTRICT`, para que o banco impeça apagar algo com histórico.

**Imutabilidade:** `mensagens` e as tabelas `historico_*` só recebem inserções. A aplicação não edita nem exclui essas linhas.

**Transações:** operações compostas (atribuir, transferir, concluir, cancelar) gravam o chamado, o histórico e as notificações em uma única transação (RNF10). Ao atribuir ou transferir, o chamado é bloqueado com `SELECT ... FOR UPDATE` para evitar duas atribuições simultâneas.

**Índices:** em `chamados` por `status`, `prioridade`, `solicitante_id`, `tec_responsavel_id`, `categoria_id`, `criado_em` e `(status, tec_responsavel_id)`; em `mensagens` e `notas_internas` por `(chamado_id, criado_em)`; em `notificacoes` por `(usuario_id, lida_em)`; em `solucoes`, índice GIN de busca textual em português (Fase 2).

## 5. Dados iniciais (seed)

Criados por comando (`flask seed`), de forma repetível:
- Perfis: colaborador, tecnico, admin.
- `prazos_prioridade`: alta 60/480, média 120/630, baixa 300/1890.
- `configuracoes`: expediente 08:00–18:30, dias úteis 1–5, limites de anexo, retenção 7 + 3 dias, alerta de 20%, bloqueio de login (5 falhas, 15 min).
- Categorias iniciais: Equipamentos (computador, monitor, teclado, impressora) e Programas (sistemas internos, navegador, e-mail).
- O primeiro administrador é criado por `flask criar-admin`.
- Para demonstração: `flask seed-demo` cria usuários e chamados de exemplo.

## 6. Anexos

Os arquivos ficam em `instance/uploads/`, fora do banco e fora de `static/`. O banco guarda nome original, nome armazenado (UUID), caminho relativo, tipo detectado, tamanho, hash, estado de preservação e data de exclusão lógica. Nunca se usa o nome original do usuário para gravar no disco.

## 7. Acesso à base e segurança

- O app usa um usuário do banco com permissões só sobre as tabelas do sistema (não o superusuário).
- Senhas e tokens são guardados como hash.
- As permissões de negócio são aplicadas na camada de aplicação; o banco reforça a integridade.

## 8. Backup

- Backup diário do PostgreSQL (`pg_dump`) e da pasta `instance/uploads/`.
- Cópias em local protegido, com teste periódico de restauração.
- Política de retenção definida na implantação.

## 9. Situação atual

Modelo lógico v2.0 fechado e validado. Próximos passos:

1. Conferir o diagrama no dbdiagram.io com o `banco.dbml`.
2. Subir o PostgreSQL local (Docker Compose).
3. Escrever os models e gerar a primeira migration.
4. Executar `flask seed` e validar relacionamentos e restrições.