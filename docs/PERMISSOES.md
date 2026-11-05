# Permissões e Segurança

## 1. Princípios

1. **Menor privilégio:** cada perfil acessa só o necessário.
2. **Validação no servidor:** toda rota e toda consulta verificam o perfil e a propriedade do dado. A interface apenas reflete essas regras.
3. **Negar por padrão:** rota sem regra explícita de acesso é negada.
4. **Rastreabilidade:** ações sensíveis e acessos negados ficam registrados.

## 2. Matriz de permissões

Legenda: **Sim** · **Não** · **Próprios** (apenas os chamados abertos pela pessoa) · **Atribuídos** (apenas os chamados sob sua responsabilidade).

| Ação | Colaborador | Técnico | Admin |
|---|---|---|---|
| Abrir chamado | Sim | Sim | Sim |
| Ver chamados | Próprios | Atribuídos + próprios | Todos |
| Enviar mensagem | Próprios (abertos) | Atribuídos (abertos) | Todos (abertos) |
| Ver notas internas | Não | Atribuídos | Todos |
| Criar nota interna | Não | Atribuídos | Todos |
| Cancelar chamado | Próprios sem técnico | Não | Qualquer sem técnico |
| Alterar status | Não | Atribuídos | Todos |
| Alterar prioridade | Não | Atribuídos | Todos |
| Informar previsão | Não | Atribuídos | Todos |
| Estender limite de resolução | Não | Não | Sim |
| Concluir chamado | Não | Atribuídos | Todos |
| Atribuir e transferir | Não | Não | Sim |
| Enviar anexo | Próprios (abertos) | Atribuídos (abertos) | Todos (abertos) |
| Baixar anexo | Próprios | Atribuídos | Todos |
| Selecionar anexos a preservar | Não | Atribuídos concluídos | Todos |
| Base de conhecimento (Fase 2) | Não | Consultar e cadastrar | Tudo |
| Dashboard | Resumo próprio | Próprio atendimento | Geral |
| Notificações | Próprias | Próprias | Próprias |
| Gerenciar usuários | Não | Não | Sim |
| Gerenciar categorias | Não | Não | Sim |
| Configurações (prazos, expediente, domínios, limites) | Não | Não | Sim |
| Ver log de segurança | Não | Não | Sim |
| Editar o próprio perfil e senha | Sim | Sim | Sim |

O perfil **admin** herda tudo o que o técnico faz.

## 3. Como implementar

- **Decorator por perfil** (`@role_required("admin")`) para barrar o acesso à rota.
- **Filtro na consulta:** o service monta a query já restrita ao usuário (ex.: colaborador → `solicitante_id = usuario.id`; técnico → `tec_responsavel_id = usuario.id OR solicitante_id = usuario.id`). Assim, trocar o ID na URL devolve **404**, não os dados de outra pessoa.
- **Funções de política** (`pode_ver_chamado`, `pode_alterar_status`...) em um único módulo, usadas pelos services e pelos templates.
- **Resposta a acesso indevido:** 404 para chamados de terceiros (não revelar que existem) e 403 para áreas administrativas.

## 4. Política de segurança

| Tema | Regra |
|---|---|
| Senhas | Mínimo de 10 caracteres; hash scrypt (padrão do Werkzeug) ou argon2 |
| Login | Bloqueio de 15 min após 5 falhas; mesma mensagem para usuário ou senha errados |
| Sessão | Cookie `HttpOnly`, `SameSite=Lax`, `Secure` em produção; expira em 8 h |
| Tokens | Aleatórios, de uso único, guardados como hash; confirmação 24 h, redefinição 1 h |
| Recuperação de senha | Resposta idêntica para e-mail existente e inexistente |
| Cadastro | Domínio autorizado, e-mail confirmado, nunca aceita o campo de perfil vindo do formulário |
| CSRF | Token em todo formulário (Flask-WTF) |
| XSS | Escape automático do Jinja; nunca usar `|safe` em conteúdo de usuário |
| SQL injection | Somente SQLAlchemy com parâmetros; nunca montar SQL por concatenação |
| Arquivos | Validação por conteúdo, nome aleatório, pasta fora de `static/`, entrega só por rota autorizada |
| Segredos | `.env` fora do Git; `.env.example` apenas com nomes |
| Cabeçalhos | `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy` básica |
| Transporte | HTTPS em produção |
| Erros | Página genérica ao usuário; detalhes só no log do servidor |
| Dados pessoais | Coleta mínima; usuários desativados em vez de excluídos |

## 5. Log de segurança

Eventos registrados em `log_seguranca`: login com sucesso, login com falha, bloqueio de conta, logout, redefinição de senha, criação e alteração de usuário, mudança de perfil, acesso negado (403 e tentativa de acesso a chamado de terceiros), alteração de configurações.

## 6. Ameaças principais e defesa

| Ameaça | Defesa |
|---|---|
| Colaborador tenta ver chamado alheio mudando o ID na URL | Consulta filtrada por perfil, resposta 404 |
| Colaborador tenta se promover a técnico no cadastro | Perfil fixado no servidor; formulário não tem esse campo |
| Colaborador acessa nota interna | Notas não são carregadas nem renderizadas para esse perfil |
| Técnico vê chamados de outros técnicos | Consulta restrita aos atribuídos |
| Upload de arquivo malicioso | Validação por conteúdo, lista de formatos, armazenamento fora de pasta pública |
| Download direto de anexo por URL | Rota única que confere permissão |
| Força bruta no login | Bloqueio temporário e registro das falhas |
| Roubo de token por vazamento do banco | Tokens guardados como hash, curta validade |
| Remoção do último administrador | Regra RN25 |