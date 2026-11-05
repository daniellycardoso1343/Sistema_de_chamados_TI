# Requisitos do Sistema

## 1. Apresentação

O Sistema de Chamados de TI centraliza as solicitações de suporte técnico de uma organização. Colaboradores registram problemas de equipamentos e programas, acompanham o andamento e conversam com a equipe de TI. A equipe de TI administra os chamados, registra soluções e acompanha prazos.

## 2. Objetivos

- Organizar as solicitações de suporte e substituir pedidos em canais informais.
- Facilitar a distribuição das demandas.
- Monitorar prazos de atribuição e de resolução.
- Manter o histórico dos atendimentos.
- Reaproveitar soluções e identificar problemas recorrentes (Fase 2).
- Reduzir a perda de informações.

## 3. Escopo

### 3.1. Incluído
Autenticação e cadastro; controle de acesso por perfil; abertura e acompanhamento de chamados; categorias e prioridades; atribuição e transferência; mensagens e notas internas; registro de solução; prazos em horas úteis; notificações; dashboard; pesquisa e filtros; anexos; histórico; base de conhecimento (Fase 2).

### 3.2. Fora do escopo
Atribuição automática; reabertura de chamados encerrados; atendimento de outros departamentos; integrações externas; diagnóstico automatizado; feriados no cálculo de prazos; pausa de prazo ("aguardando usuário"); prioridade Crítica.

## 4. Perfis

| Perfil | Descrição |
|---|---|
| **Colaborador** | Abre e acompanha os próprios chamados. Nunca vê chamados de terceiros nem notas internas. |
| **Técnico** | Atende os chamados atribuídos a ele. Não distribui chamados. |
| **Administrador** | Distribui chamados, gerencia usuários e configurações, enxerga tudo e também atua como técnico. |

Os três perfis são fixos. Não há permissões granulares nesta versão. Detalhes em [PERMISSOES.md](PERMISSOES.md).

## 5. Requisitos funcionais

Legenda de fase: **M** = MVP · **2** = Fase 2.

| ID | Requisito | Fase |
|---|---|---|
| RF01 | **Autenticação.** Login e logout com credenciais; sessão com expiração; bloqueio temporário após falhas consecutivas. | M |
| RF02 | **Gerenciamento de usuários.** O administrador cadastra, consulta, edita, ativa, desativa e altera o perfil de contas. | M |
| RF03 | **Controle de permissões.** Acesso a funções e dados conforme o perfil (ver PERMISSOES.md). | M |
| RF04 | **Abertura de chamados.** Título, descrição, categoria, prioridade desejada e anexos opcionais. Gera número de protocolo. | M |
| RF05 | **Categorização.** Categorias e subcategorias administráveis, sem alterar código. Categorias em uso são desativadas, não excluídas. | M |
| RF06 | **Consulta de chamados.** Cada perfil vê apenas o seu escopo, com status, prioridade, responsável e prazos. | M |
| RF07 | **Atribuição.** O administrador atribui um chamado a um técnico (ou a si mesmo). | M |
| RF08 | **Transferência.** O administrador transfere um chamado entre técnicos, preservando histórico, mensagens, anexos e prazos. | M |
| RF09 | **Atualização de status.** Aberto, Em atendimento, Concluído e Cancelado, conforme as transições permitidas. | M |
| RF10 | **Alteração de prioridade.** Técnico responsável ou administrador, com justificativa, registrada no histórico. | M |
| RF11 | **Comunicação no chamado.** Troca de mensagens entre solicitante e equipe de TI. | M |
| RF12 | **Notas internas.** Observações visíveis só para técnico responsável e administrador. | M |
| RF13 | **Registro de solução.** A solução aplicada é obrigatória para concluir o chamado e fica visível ao solicitante. | M |
| RF14 | **Base de conhecimento.** Cadastro e consulta de soluções reutilizáveis pela equipe de TI. | 2 |
| RF15 | **Gerenciamento de anexos.** Envio e consulta respeitando permissões e limites. | M |
| RF16 | **Seleção de anexos para preservação.** Após o prazo de retenção, o técnico escolhe quais anexos manter. | 2 |
| RF17 | **Exclusão automática de anexos.** Remove os não selecionados após a tolerância. | 2 |
| RF18 | **Definição de prazos.** Cálculo do prazo de atribuição e do limite de resolução em horas úteis; previsão informada pelo técnico dentro do limite. | M |
| RF19 | **Notificações.** No sistema (M) e por e-mail (2) para os eventos listados em REGRAS_DE_NEGOCIO.md. | M / 2 |
| RF20 | **Histórico de alterações.** Registra status, prioridade, prazo e responsável, com autor, data e hora. | M |
| RF21 | **Acompanhamento de prazos.** Identifica chamados próximos do vencimento (menos de 20% do prazo restante) e vencidos. | M |
| RF22 | **Recuperação de senha.** Token enviado por e-mail, com validade e uso único. | M |
| RF23 | **Cadastro de colaboradores.** Autocadastro somente com e-mail de domínio autorizado; nunca concede perfil de técnico ou administrador. | M |
| RF24 | **Confirmação de e-mail.** A conta só é ativada após a confirmação. | M |
| RF25 | **Dashboard.** Indicadores por perfil (ver abaixo). | M |
| RF26 | **Pesquisa e filtros de chamados.** Por número, título, status, prioridade, categoria, técnico, data de abertura e prazo. | M |
| RF27 | **Pesquisa na base de conhecimento.** Por título e palavras do conteúdo. | 2 |
| RF28 | **Controle do prazo de atribuição.** Alerta o administrador quando o prazo para atribuir está próximo ou vencido. | M (indicador) / 2 (alerta automático) |
| RF29 | **Cancelamento de chamado.** O solicitante (ou o administrador) cancela um chamado ainda não atribuído. | M |
| RF30 | **Configurações do sistema.** O administrador edita prazos por prioridade, expediente, limites de anexo e domínios autorizados. | M |
| RF31 | **Chamados relacionados e recorrência.** Vínculo entre chamados e registro da solução usada, para identificar problemas frequentes. | 2 |

### Indicadores do dashboard (RF25)

- **Técnico:** chamados atribuídos; abertos e em atendimento; próximos do vencimento; vencidos; concluídos no período.
- **Administrador:** total de chamados; sem técnico; por prioridade e por status; por técnico; atrasados.
- **Colaborador:** resumo dos próprios chamados por status.

## 6. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | **Senhas** armazenadas com hash apropriado (scrypt/argon2). Nunca em texto puro. |
| RNF02 | **Tokens** de confirmação e recuperação com validade curta, uso único e armazenados como hash. |
| RNF03 | **Controle de acesso no servidor** para páginas, operações, mensagens, chamados e arquivos. Esconder botões não é controle de acesso. |
| RNF04 | **Validação de arquivos** no servidor por conteúdo, tamanho e formato, nunca só pela extensão. |
| RNF05 | **Armazenamento de arquivos** fora do banco e fora de pastas públicas. |
| RNF06 | **Integridade do histórico:** transferências, prioridade, status e prazos preservam dados para auditoria. |
| RNF07 | **Usabilidade:** abrir e acompanhar chamados de forma simples; painéis claros. |
| RNF08 | **Manutenibilidade:** módulos com responsabilidades definidas (routes, services, models). |
| RNF09 | **Tratamento de erros** sem expor detalhes técnicos ao usuário. |
| RNF10 | **Integridade das operações:** alterações relacionadas ocorrem em uma única transação (ex.: atribuir + registrar histórico + notificar). |
| RNF11 | **Limites de anexos:** 10 MB por arquivo, 5 por envio, 50 MB por chamado. |
| RNF12 | **Compatibilidade:** navegadores modernos e interface responsiva. |
| RNF13 | **Desempenho:** metas numéricas a definir após a implantação; listas sempre paginadas. |
| RNF14 | **Portabilidade:** executar em Linux e Windows, com opção de Docker Compose. |
| RNF15 | **Auditoria de segurança:** registrar logins, falhas, acessos negados e alterações de usuários. |
| RNF16 | **Fuso horário:** datas em UTC no banco, exibidas em America/Sao_Paulo. |
| RNF17 | **Proteção contra CSRF e XSS** em todos os formulários e páginas. |
| RNF18 | **Privacidade (LGPD):** coletar apenas dados necessários; usuários são desativados, não apagados. |

## 7. Mapa de mudanças em relação à versão 1.0

| Antes | Agora |
|---|---|
| RF08 duplicado (transferência e status) | Transferência = RF08; status = RF09; os demais avançam +1 (28 RFs corrigidos) |
| "RN011" | RN11 |
| "Gerenciar permissões" (admin) | "Alterar o perfil de um usuário" (RF02) |
| RF15, RF16 e RN22 conflitantes | Linha do tempo única em REGRAS_DE_NEGOCIO.md |
| RN21 com frase solta | Extensão de prazo só por autorização explícita do administrador, com justificativa |
| Sem cancelamento, configurações e recorrência | RF29, RF30 e RF31 |