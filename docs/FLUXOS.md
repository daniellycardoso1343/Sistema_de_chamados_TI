# Fluxos do Sistema

Os diagramas usam Mermaid e são exibidos automaticamente no GitHub.

## 1. Ciclo de vida do chamado

```mermaid
stateDiagram-v2
    [*] --> aberto: colaborador abre
    aberto --> cancelado: solicitante ou admin (sem técnico)
    aberto --> em_atendimento: técnico inicia (após atribuição)
    em_atendimento --> concluido: técnico ou admin (solução obrigatória)
    cancelado --> [*]
    concluido --> [*]
```

Chamados `cancelado` e `concluido` são finais: sem reabertura e sem novas mensagens.

## 2. Abertura e atribuição

```mermaid
flowchart TD
    A[Colaborador preenche o formulário] --> B[Sistema valida e gera o protocolo]
    B --> C[Status = aberto]
    C --> D[Calcula prazo de atribuição em horas úteis]
    D --> E[Notifica administradores]
    E --> F[Admin escolhe o técnico]
    F --> G{Técnico é o próprio solicitante?}
    G -- Sim --> H[Recusa a atribuição]
    G -- Não --> I[Na mesma transação: grava técnico e atribuido_em, calcula limite de resolução, registra historico_atribuicoes, cria notificações]
```

## 3. Transferência

```mermaid
flowchart TD
    A[Admin escolhe novo técnico e informa justificativa] --> B{Novo técnico é o solicitante?}
    B -- Sim --> X[Recusa]
    B -- Não --> C[Atualiza tec_responsavel_id]
    C --> D[atribuido_em e limite_resolucao permanecem inalterados]
    D --> E[Registra historico_atribuicoes]
    E --> F[Notifica técnico anterior, novo técnico e solicitante]
```

## 4. Atendimento e conclusão

```mermaid
flowchart TD
    A[Técnico abre o chamado] --> B[Informa previsão de conclusão]
    B --> C{Previsão menor ou igual ao limite?}
    C -- Não --> B
    C -- Sim --> D[Registra historico_prazos]
    D --> E[Conversa com o solicitante e registra notas internas]
    E --> F[Preenche a solução aplicada]
    F --> G[Conclui]
    G --> H[Status = concluido, grava encerrado_em, notifica o solicitante]
```

## 5. Cadastro e confirmação de e-mail

```mermaid
flowchart TD
    A[Visitante informa nome, e-mail e senha] --> B{Domínio autorizado?}
    B -- Não --> X[Recusa]
    B -- Sim --> C[Cria usuário com perfil colaborador, inativo]
    C --> D[Gera token de 24 h e envia por e-mail]
    D --> E[Usuário clica no link]
    E --> F{Token válido, não usado e não expirado?}
    F -- Não --> Y[Informa erro e permite reenvio]
    F -- Sim --> G[Confirma e-mail, ativa a conta, invalida o token]
```

## 6. Recuperação de senha

```mermaid
flowchart TD
    A[Usuário informa o e-mail] --> B[Resposta genérica, exista ou não a conta]
    B --> C[Se existir: gera token de 1 h e envia]
    C --> D[Usuário abre o link e define nova senha]
    D --> E{Token válido?}
    E -- Não --> X[Erro]
    E -- Sim --> F[Grava hash da nova senha, invalida o token, registra no log]
```

## 7. Retenção de anexos (Fase 2)

```mermaid
flowchart TD
    A[Chamado concluído, D0] --> B[Anexos disponíveis por 7 dias]
    B --> C[D+7: notifica técnico responsável ou admin]
    C --> D[Técnico seleciona os anexos a preservar]
    D --> E[D+10: worker exclui os não selecionados]
    C --> E
    E --> F[Arquivo removido do disco, registro mantido com excluido_em]
```

## 8. Entrega de anexo

```mermaid
flowchart LR
    A[Usuário clica em baixar] --> B[Rota /anexos/id/download]
    B --> C{Pode ver o chamado deste anexo?}
    C -- Não --> X[404]
    C -- Sim --> D{Anexo foi excluído?}
    D -- Sim --> Y[Informa que o arquivo foi removido]
    D -- Não --> E[Envia o arquivo]
```
