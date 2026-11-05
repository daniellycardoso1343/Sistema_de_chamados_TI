# Regras de Negócio

## 1. Prioridades e prazos

Existem três prioridades. Todos os prazos são contados em **minutos úteis** e são configuráveis pelo administrador (tabela `prazos_prioridade`).

| Prioridade | Atribuir em até | Resolver em até | Em minutos úteis (atribuição / resolução) |
|---|---|---|---|
| Alta | 1 hora | 8 horas | 60 / 480 |
| Média | 2 horas | 1 dia útil | 120 / 630 |
| Baixa | 5 horas | 3 dias úteis | 300 / 1890 |

**Expediente:** segunda a sexta, 08:00 às 18:30 (630 minutos por dia). Feriados não são considerados nesta versão. "1 dia útil" equivale a 630 minutos úteis, ou seja, o mesmo horário do próximo dia útil.

## 2. Os três prazos de um chamado

| Prazo | Quem define | Quando começa a contar | Campo |
|---|---|---|---|
| **Prazo de atribuição** | Sistema | Na abertura do chamado | `prazo_atribuicao` |
| **Limite de resolução** | Sistema | Na primeira atribuição a um técnico | `limite_resolucao` |
| **Previsão de conclusão** | Técnico responsável | Quando ele informa | `previsao_conclusao` |

Regras:

- A previsão nunca pode ultrapassar o limite de resolução.
- A transferência entre técnicos **não** reinicia nem prolonga o limite. A contagem continua a partir da atribuição original (`atribuido_em`).
- Somente o **administrador** pode estender o limite, em caráter excepcional, informando uma justificativa. A extensão é registrada em `historico_prazos`.
- Se a prioridade mudar depois da atribuição, o limite é recalculado a partir da atribuição original com a nova prioridade. Se a previsão do técnico ficar acima do novo limite, ele deve informar uma nova previsão com justificativa.
- Toda alteração de prazo gera registro em `historico_prazos`.

### Cálculo em horas úteis

1. Se o instante inicial está fora do expediente (noite, fim de semana), ele é movido para a próxima abertura (08:00 do próximo dia útil).
2. Soma-se o prazo em minutos, consumindo os minutos úteis de cada dia; o que sobra passa para o próximo dia útil, a partir das 08:00.

Exemplos validados:

| Situação | Resultado |
|---|---|
| Média aberta na segunda às 16:00 | Prazo de atribuição: segunda 18:00 |
| Média atribuída na segunda às 17:00 | Limite de resolução: terça 17:00 |
| Baixa atribuída na segunda às 16:00 | Limite de resolução: quinta 16:00 |
| Alta atribuída na sexta às 17:00 | Limite de resolução: segunda 14:30 |
| Alta aberta no sábado às 10:00 | Prazo de atribuição: segunda 09:00 |
| Alta aberta na segunda às 18:30 | Prazo de atribuição: terça 09:00 |

### Prazo próximo do vencimento

Um prazo é considerado **próximo** quando restam menos de **20%** do tempo total previsto para aquela prioridade, medido em minutos úteis. Passou do limite, é **vencido**.

## 3. Estados do chamado

| Status | Significado |
|---|---|
| `aberto` | Registrado, aguardando atribuição (ou atribuído e ainda não iniciado) |
| `em_atendimento` | Técnico trabalhando |
| `concluido` | Solução registrada e chamado encerrado |
| `cancelado` | Cancelado pelo solicitante ou pelo administrador antes de ser atribuído |

| De | Para | Quem | Condição |
|---|---|---|---|
| (novo) | aberto | Solicitante | Sempre |
| aberto | em_atendimento | Técnico responsável ou admin | Chamado atribuído |
| aberto | cancelado | Solicitante ou admin | Sem técnico atribuído |
| em_atendimento | concluido | Técnico responsável ou admin | `solucao_aplicada` preenchida |

Qualquer outra transição é recusada. Chamados `concluido` e `cancelado` são **finais**: não podem ser reabertos nem receber novas mensagens. Se o problema voltar, abre-se um novo chamado, que pode ser vinculado ao anterior (Fase 2).

## 4. Atribuição e transferência

- Todo chamado novo nasce `aberto` e sem técnico.
- Somente o administrador atribui e transfere. Ele pode atribuir a si mesmo.
- **Ninguém pode ser responsável por um chamado que ele próprio abriu.**
- A transferência registra técnico anterior, novo técnico, administrador, justificativa, data e hora, e não apaga nem duplica mensagens, anexos ou histórico.
- Não é possível desativar um técnico com chamados abertos sob sua responsabilidade; é preciso transferir antes.
- O último administrador ativo não pode ser desativado nem ter o perfil alterado.

## 5. Conclusão

Só o técnico responsável ou o administrador conclui. A solução aplicada é obrigatória e fica visível ao solicitante. A conclusão é imediata e irreversível.

## 6. Anexos

### Limites e formatos

| Regra | Valor |
|---|---|
| Tamanho por arquivo | 10 MB |
| Arquivos por envio | 5 |
| Tamanho total por chamado | 50 MB |
| Formatos permitidos | pdf, png, jpg, txt, log, docx, xlsx |
| Formatos bloqueados | executáveis, scripts, arquivos compactados |

A validação é feita no servidor pelo conteúdo real do arquivo. O arquivo é gravado com nome aleatório fora de pasta pública e só é entregue por rota que confere a permissão.

### Retenção (Fase 2 para a automação)

| Momento | O que acontece |
|---|---|
| D0: chamado concluído | Anexos continuam disponíveis. O técnico pode selecionar o que preservar a qualquer momento. |
| D+7 | O sistema notifica o técnico responsável (ou o admin, se o técnico estiver inativo) para selecionar os anexos a preservar. |
| D+10 (3 dias de tolerância) | Anexos não selecionados são excluídos: o arquivo físico é removido, e o registro permanece com `excluido_em`. |

Chamados cancelados seguem a mesma contagem, sem etapa de seleção. No MVP não há exclusão automática: os anexos permanecem.

## 7. Notificações

| Evento | Destinatário | Canal MVP | Canal Fase 2 |
|---|---|---|---|
| Chamado aberto | Administradores | Sistema | + E-mail |
| Chamado atribuído ou transferido | Novo técnico (e o anterior, na transferência) e solicitante | Sistema | + E-mail |
| Nova mensagem | A outra parte (solicitante ou técnico) | Sistema | + E-mail |
| Status alterado, concluído ou cancelado | Solicitante (e técnico, no cancelamento) | Sistema | + E-mail |
| Prioridade alterada | Solicitante | Sistema | + E-mail |
| Prazo de atribuição próximo ou vencido | Administradores | Indicador no painel | Notificação + E-mail |
| Prazo de resolução próximo ou vencido | Técnico responsável e administradores | Indicador no painel | Notificação + E-mail |
| Seleção de anexos solicitada | Técnico responsável | Não se aplica | Sistema + E-mail |

Notas internas nunca geram notificação ao solicitante. Falha no envio de e-mail não pode impedir a ação do usuário.

## 8. Contas, senhas e tokens

- O autocadastro só aceita e-mail de **domínio autorizado** (cadastrado pelo admin). Técnicos e administradores são criados exclusivamente pelo administrador. O primeiro administrador é criado por comando de linha.
- A conta só fica ativa após a confirmação do e-mail.
- Senha: mínimo de 10 caracteres.
- Após 5 tentativas de login com falha, a conta fica bloqueada por 15 minutos.
- Token de confirmação de e-mail: válido por 24 horas. Token de redefinição de senha: válido por 1 hora. Ambos de uso único.
- A recuperação de senha responde da mesma forma para e-mails existentes e inexistentes.
- Sessão expira após 8 horas.
- Usuários nunca são excluídos, apenas desativados.

## 9. Lista consolidada de regras

| ID | Regra |
|---|---|
| RN01 | Todo acesso exige conta autenticada; as funções dependem do perfil. |
| RN02 | A abertura registra automaticamente data e hora e gera o número do protocolo. |
| RN03 | O solicitante pode anexar arquivos dentro dos limites e formatos permitidos. |
| RN04 | Todo chamado novo nasce `aberto` e aguarda atribuição pelo administrador. |
| RN05 | O administrador atribui chamados e também pode atender como técnico. |
| RN06 | O técnico informa a previsão de conclusão, limitada ao limite da prioridade. |
| RN07 | Todo chamado deve ser atribuído dentro do prazo de atribuição da sua prioridade. |
| RN08 | O limite de resolução conta a partir da primeira atribuição; os dois prazos são controlados separadamente. |
| RN09 | O sistema impede previsões acima do limite definido para a prioridade. |
| RN10 | Os prazos usam horas úteis (seg–sex, 08:00–18:30); feriados ficam para versão futura. |
| RN11 | O colaborador informa a prioridade desejada; a equipe de TI pode alterá-la, com justificativa e registro no histórico. |
| RN12 | Mensagens permanecem no histórico; notas internas são exclusivas da equipe de TI. |
| RN13 | O técnico conclui após registrar a solução; a conclusão encerra o chamado imediatamente. |
| RN14 | Chamado encerrado (concluído ou cancelado) não pode ser reaberto. |
| RN15 | O histórico de chamados encerrados é preservado e consultável conforme as permissões. |
| RN16 | A equipe de TI mantém uma base de soluções reutilizáveis (Fase 2). |
| RN17 | O sistema notifica os eventos da seção 7. |
| RN18 | Colaboradores só veem os próprios chamados; técnicos só os atribuídos; administradores veem todos. |
| RN19 | O administrador distribui os chamados e gerencia as configurações. |
| RN20 | A transferência registra anterior, novo responsável, administrador, data e hora, e preserva todo o conteúdo. |
| RN21 | A transferência não reinicia nem prolonga o limite; só o administrador pode estendê-lo, com justificativa. |
| RN22 | Anexos seguem a linha do tempo de retenção da seção 6. |
| RN23 | Anexos só são entregues após conferência de permissão no servidor. |
| RN24 | Ninguém pode ser responsável pelo próprio chamado. |
| RN25 | Técnico com chamados abertos não pode ser desativado; o último administrador ativo não pode ser desativado nem rebaixado. |
| RN26 | Só e-mails de domínios autorizados podem se cadastrar; perfis elevados são concedidos apenas pelo administrador. |
| RN27 | Cancelamento só é possível enquanto o chamado não tem técnico atribuído. |
| RN28 | Um prazo é "próximo" quando restam menos de 20% do tempo total da prioridade. |