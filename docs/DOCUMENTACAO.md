# Sistema de gestão de chamados
Documento de Requisitos de Software
Versão: 1.0 — Em elaboração
Status: Levantamento e especificação de requisitos
Objetivo: Documentar os requisitos e as regras do sistema antes da modelagem do banco de dados.

# APRESENTAÇÃO DO PROJETO
O Sistema de Gerenciamento de Chamados de TI será uma aplicação web destinada a centralizar e organizar as solicitações de suporte técnico de uma organização.
A aplicação permitirá que colaboradores registrem problemas relacionados a equipamentos e programas, acompanhem o andamento de suas solicitações e se comuniquem com a equipe de Tecnologia da Informação (TI).
A equipe de TI poderá administrar os chamados, registrar soluções, acompanhar prazos e consultar uma base de conhecimento interna. O sistema também contará com recursos de notificação, pesquisa, indicadores e controle de acesso.

# OBJETIVO DO PROJETO
O objetivo desse projeto é centralizar os chamados e as demandas de suporte técnico para usuários, substituir pedidos dispersos de ajuda em canais informais. Os resultados esperados são os seguintes:
Organizar as solicitações de suporte;
Facilitar a distribuição de demandas;
Monitorar os prazos de resolução;
Manter o histórico dos atendimentos;
Identificar chamados recorrentes e reutilizar soluções já documentadas anteriormente; 
Reduzir a perda de informações.

# ESCOPO DO SISTEMA
## 3.1. Funcionalidades incluídas
A primeira versão do sistema deverá contemplar:
Autenticação e gerenciamento de usuários.
Cadastro de colaboradores com e-mail empresarial.
Recuperação de senha por e-mail.
Controle de acesso por perfil.
Abertura e acompanhamento de chamados.
Classificação por categoria e prioridade.
Atribuição manual de chamados.
Transferência de chamados entre técnicos.
Comunicação entre colaborador e equipe de TI.
Registro de notas internas.
Registro de soluções aplicadas.
Controle de prazos de atendimento.
Notificações no sistema e por e-mail.
Painéis de indicadores.
Pesquisa e filtros de chamados.
Base de conhecimento interna.
Gerenciamento e retenção de anexos.
Histórico de alterações.

## 3.2. Fora do escopo inicial
As seguintes funcionalidades não fazem parte do escopo confirmado da primeira versão:
Atribuição automática de chamados.
Reabertura de chamados encerrados.
Atendimento de solicitações de outros departamentos que não sejam de TI.
Integrações com ferramentas externas de suporte.
Automatizações avançadas de diagnóstico.
Essas funcionalidades poderão ser avaliadas em versões futuras.
 Perfis de usuário

## 4.1. Colaborador
Usuário responsável por registrar solicitações de suporte.
Permissões previstas:
Criar uma conta utilizando e-mail empresarial autorizado.
Confirmar seu endereço de e-mail.
Autenticar-se no sistema.
Solicitar redefinição de senha.
Abrir chamados.
Consultar os próprios chamados.
Acompanhar o andamento das solicitações.
Enviar mensagens e anexos nos próprios chamados.
Consultar notificações relacionadas às suas solicitações.
O colaborador não poderá acessar chamados de outros usuários nem visualizar notas internas da equipe de TI.

## 4.2. Técnico de TI
Usuário responsável pelo atendimento das solicitações.
Permissões previstas:
Consultar chamados conforme as permissões estabelecidas.
Visualizar os chamados atribuídos a si.
Atualizar o andamento dos chamados.
Enviar mensagens aos colaboradores.
Registrar notas internas.
Alterar prioridades, quando autorizado.
Registrar soluções aplicadas.
Consultar a base de conhecimento.
Cadastrar soluções reutilizáveis.
Consultar indicadores relacionados ao próprio atendimento.
Selecionar anexos para preservação.

## 4.3. Administrador
Usuário responsável pela administração do sistema e pela distribuição das demandas.
Permissões previstas:
Gerenciar contas de usuários.
Gerenciar permissões.
Consultar os chamados do sistema.
Atribuir chamados manualmente.
Transferir chamados entre técnicos.
Administrar categorias e subcategorias.
Consultar indicadores gerais.
Acompanhar prazos e atrasos.
Administrar configurações do sistema.
Atuar também como técnico de TI.



# REQUISITOS FUNCIONAIS

RF01 — Autenticação de usuários
O sistema deverá permitir que os usuários façam login com suas credenciais para acessar as funcionalidades autorizadas ao seu perfil.

RF02 — Gerenciamento de usuários
O administrador deverá poder cadastrar, consultar, editar, ativar e desativar contas de usuários.

RF03 — Controle de permissões
O sistema deverá controlar o acesso às funcionalidades de acordo com o perfil do usuário:
Colaborador: abre chamados e acompanha os próprios chamados.
Técnico de TI: consulta e atende chamados conforme suas permissões.
Administrador: gerencia o sistema, distribui chamados e também pode atuar como 
técnico.

RF04 — Abertura de chamados
O sistema deverá permitir que os colaboradores registrem chamados de suporte técnico, informando, no mínimo:
Título;
Descrição do problema;
Categoria;
Prioridade desejada;
Anexos, quando necessário.

RF05 — Categorização de chamados
O sistema deverá permitir classificar os chamados por categoria, como:
Equipamentos: computador, monitor, teclado e outros dispositivos.
Programas: sistemas internos, navegadores e outros softwares.
As categorias e subcategorias deverão ser administráveis, evitando que seja necessário alterar o código sempre que uma nova opção for criada.

RF06 — Consulta de chamados
O sistema deverá permitir que os colaboradores consultem seus próprios chamados e acompanhem informações como status, prioridade, técnico responsável e prazo de resolução.
Os técnicos deverão consultar os chamados que estejam autorizados a visualizar, enquanto o administrador poderá consultar os chamados necessários à gestão do sistema.

RF07 — Atribuição de chamados
O sistema deverá permitir que o administrador atribua manualmente um chamado a um técnico responsável.
RF08 — Transferência de chamados
O sistema deverá permitir que o administrador transfira um chamado de um técnico para outro, preservando o histórico, as mensagens e os anexos associados.

RF08 — Atualização do status
O sistema deverá permitir que os usuários autorizados atualizem o status dos chamados.
Os status inicialmente previstos são:
Aberto;
Em atendimento;
Concluído/encerrado.

RF09 — Alteração de prioridade
O sistema deverá permitir que usuários autorizados da equipe de TI alterem a prioridade de um chamado, registrando a alteração no histórico.

RF10 — Comunicação no chamado
O sistema deverá permitir a troca de mensagens entre o colaborador e a equipe de TI dentro do próprio chamado.

RF11 — Registro de notas internas
O sistema deverá permitir que os técnicos registrem observações internas, visíveis somente para usuários autorizados da equipe de TI.

RF12 — Registro de solução
O sistema deverá permitir que o técnico registre a solução aplicada antes de concluir o chamado.

RF13 — Base de conhecimento
O sistema deverá disponibilizar uma base interna de conhecimento para a equipe de TI, permitindo consultar e cadastrar soluções reutilizáveis para problemas recorrentes.

RF14 — Gerenciamento de anexos
O sistema deverá permitir o envio e a consulta de arquivos associados aos chamados, respeitando as permissões de acesso e os limites de armazenamento definidos.

RF15 — Seleção de anexos para preservação
Após o encerramento de um chamado, o sistema deverá solicitar ao técnico responsável que selecione quais anexos devem ser preservados, de acordo com a política de retenção definida.

RF16 — Exclusão automática de anexos não selecionados
O sistema deverá excluir automaticamente os anexos que não forem selecionados para preservação após o prazo de decisão e a tolerância definidos.

RF17 — Definição de prazo de resolução
O sistema deverá calcular e acompanhar o prazo de resolução do chamado considerando sua prioridade, o horário útil de atendimento e a data inicial da atribuição ao técnico.

RF18 — Notificações
O sistema deverá notificar os usuários sobre eventos relevantes, incluindo:
Abertura de chamados;
Atribuição ou transferência de chamados;
Alterações relevantes no chamado;
Mensagens recebidas;
Solicitações de seleção de anexos;
Lembretes relacionados a prazos.
As notificações poderão ser apresentadas no próprio sistema e enviadas por e-mail.

RF19 — Histórico de alterações
O sistema deverá manter um histórico das principais ações realizadas nos chamados, incluindo mudanças de status, prioridade, prazo e responsável, identificando o usuário que realizou cada ação e a data e hora correspondentes.

RF20 — Acompanhamento de prazos
O sistema deverá permitir que os usuários autorizados acompanhem os prazos de resolução e identifiquem chamados próximos do vencimento ou com prazo excedido.

RF21 — Recuperação de senha
O sistema deverá permitir que o usuário solicite a redefinição de sua senha por meio de um token enviado ao e-mail cadastrado.
Regras de segurança:
O token deverá ter prazo de validade.
O token deverá ser de uso único.
Após a redefinição, o token deverá ser invalidado.
A senha deverá ser armazenada como hash seguro, nunca em texto puro.

RF22 — Cadastro de colaboradores
O sistema deverá permitir que colaboradores criem suas próprias contas utilizando exclusivamente um endereço de e-mail empresarial autorizado.
O usuário receberá um token de confirmação para garantir que a conta é usada por ele. 
O cadastro não deverá permitir que o próprio usuário conceda a si mesmo as permissões de técnico ou administrador.

RF23 — Confirmação de e-mail
O sistema deverá enviar uma mensagem de confirmação ao endereço informado durante o cadastro e permitir a ativação da conta após a validação do endereço.

RF24 — Painel de indicadores
O sistema deverá disponibilizar um painel com indicadores de atendimento, respeitando as permissões de cada perfil.
Para o técnico:
Total de chamados atribuídos a ele;
Chamados abertos e em atendimento;
Chamados próximos do vencimento;
Chamados com prazo excedido;
Chamados concluídos em determinado período.
Para o administrador:
Total de chamados do sistema;
Chamados sem técnico atribuído;
Chamados por prioridade e status;
Quantidade de chamados por técnico;
Chamados atrasados;

RF25 — Pesquisa e filtros de chamados
O sistema deverá permitir que os usuários autorizados pesquisem e filtrem chamados por critérios como:
Número ou identificador do chamado;
Título;
Status;
Prioridade;
Categoria;
Técnico responsável;
Data de abertura;
Prazo de resolução.

RF26 — Pesquisa na base de conhecimento
O sistema deverá permitir pesquisar soluções pelo título e por palavras contidas no material cadastrado.

RF27 — Controle do prazo de atribuição
O sistema deverá monitorar o tempo entre a abertura do chamado e sua primeira atribuição a um técnico, alertando o administrador quando o prazo estiver próximo do vencimento ou for ultrapassado.

## REQUISITOS NÃO FUNCIONAIS
RNF01 — Segurança de senhas
As senhas deverão ser armazenadas utilizando um algoritmo seguro de hash apropriado para senhas.
O sistema não deverá armazenar senhas em texto puro.

RNF02 — Segurança de tokens
Os tokens de confirmação de e-mail e de recuperação de senha deverão possuir validade limitada e ser invalidados após o uso.

RNF03 — Controle de acesso
O sistema deverá validar as permissões no servidor, impedindo o acesso não autorizado a páginas, operações, mensagens, chamados e arquivos.

RNF04 — Validação de arquivos
Os arquivos enviados deverão ser validados no servidor quanto ao formato, tamanho e demais restrições de segurança.
A validação não deverá depender exclusivamente da extensão do arquivo ou das verificações realizadas no navegador.

RNF05 — Armazenamento de arquivos
Os arquivos anexados deverão ser armazenados separadamente do banco de dados.
O banco deverá manter as informações necessárias para identificar e localizar os arquivos.

RNF06 — Integridade do histórico
As operações de transferência, alteração de prioridade, mudança de status e atualização de prazo deverão preservar informações suficientes para auditoria.

RNF07 — Usabilidade
A interface deverá permitir que os colaboradores abram e acompanhem chamados de maneira simples e intuitiva.
Os painéis deverão apresentar informações de forma clara, facilitando a identificação de pendências e atrasos.

RNF08 — Manutenibilidade
O código deverá ser organizado em módulos com responsabilidades definidas, facilitando a manutenção e a implementação de novas funcionalidades.

RNF09 — Tratamento de erros
O sistema deverá tratar erros de validação, falhas de comunicação e situações inesperadas sem expor informações técnicas sensíveis aos usuários.

RNF10 — Integridade das operações
O sistema deverá evitar inconsistências em operações que envolvam alterações relacionadas, como a atribuição de um chamado e o registro de seu histórico.

RNF11 — Limites de anexos
O sistema deverá impor os limites definidos para tamanho individual, quantidade e tamanho total dos anexos.

RNF12 — Compatibilidade
A aplicação deverá funcionar adequadamente em navegadores modernos e oferecer uma interface responsiva para diferentes tamanhos de tela.

RNF13 — Desempenho
O sistema deverá apresentar tempos de resposta adequados para as operações habituais de abertura, consulta, pesquisa e atualização de chamados.
Os objetivos numéricos de desempenho deverão ser definidos posteriormente, conforme as necessidades e a infraestrutura disponível.


## REGRAS DE NEGÓCIO
RN01 — Autenticação
Todos os usuários deverão possuir uma conta para acessar o sistema. As funcionalidades disponíveis dependerão do perfil e das permissões atribuídas.

RN02 — Abertura de chamados
Os colaboradores poderão registrar chamados informando título, descrição, categoria e prioridade. A data e a hora da abertura serão registradas automaticamente.

RN03 — Anexos
O solicitante poderá anexar arquivos ao chamado, respeitando os formatos, limites de tamanho e regras de segurança definidos pelo sistema.

RN04 — Distribuição dos chamados
Todo chamado novo será registrado com status Aberto e aguardará a atribuição de um técnico pelo administrador.

RN05 — Responsável pelo atendimento
O administrador poderá atribuir um chamado a um técnico. O administrador também poderá atuar como técnico e realizar atendimentos.

RN06 — Definição de prazo
O técnico responsável definirá manualmente a previsão de conclusão, respeitando o limite máximo estabelecido para a prioridade vigente.

RN07 — Prazo de atribuição
Todo chamado aberto deverá ser atribuído a um técnico pelo administrador dentro do prazo máximo estabelecido para sua prioridade.

RN08 — Prazo de resolução
O prazo máximo de resolução será contado a partir da atribuição do chamado ao técnico responsável.
O sistema deverá controlar separadamente o tempo de espera pela atribuição e o tempo de resolução após a atribuição.

RN09 — Tempo Limite
Cada prioridade terá um prazo máximo permitido para a finalização da demanda. O sistema deverá validar esses prazos informados pelo técnico e garantir que esse prazo nao exceda o limite pré estabelecido.

RN10 — Cálculo em horas úteis
Os prazos serão calculados considerando o expediente configurado no sistema. O tratamento de feriados poderá ser implementado posteriormente.

RN011 — Alteração de prioridade
O colaborador poderá informar a prioridade desejada na abertura. Usuários autorizados da equipe de TI poderão alterá-la. Toda alteração deverá ser registrada no histórico.

RN12 — Comunicação
As mensagens trocadas durante o atendimento deverão permanecer registradas no histórico do chamado. O sistema poderá oferecer registros internos exclusivos para a equipe de TI.

RN13 — Encerramento
O técnico poderá concluir o chamado após registrar a solução aplicada. A conclusão encerrará imediatamente a solicitação.

RN14 — Imutabilidade do encerramento
Um chamado encerrado não poderá ser reaberto. Se o problema persistir ou voltar a ocorrer, deverá ser aberto um novo chamado.

RN15 — Histórico
O sistema deverá preservar o histórico dos chamados encerrados para consulta posterior, respeitando as permissões de acesso.

RN16 — Biblioteca de soluções
A equipe de TI poderá consultar uma biblioteca interna de soluções. Os técnicos poderão registrar procedimentos reutilizáveis a partir dos atendimentos realizados.

RN17 — Notificações
O sistema deverá disponibilizar notificações na plataforma e enviar e-mails para os eventos definidos, incluindo os novos chamados e as atualizações relevantes do atendimento.

RN18 — Controle de acesso
Os colaboradores poderão consultar os próprios chamados. A consulta de chamados de outros colaboradores, as funções administrativas e a biblioteca técnica dependerão das permissões do usuário.

RN19 — Responsabilidade administrativa
O administrador será responsável pela distribuição dos chamados e pela gestão das configurações administrativas. Também poderá executar atividades técnicas.

RN20 — Transferência de responsabilidade
O administrador poderá transferir um chamado de um técnico para outro. A transferência deverá registrar o técnico anterior, o novo responsável, o administrador que realizou a operação, a data e a hora da transferência.
A transferência não deverá apagar nem duplicar o histórico, as mensagens, os anexos ou as demais informações do chamado. O novo responsável deverá ter acesso ao histórico necessário para dar continuidade ao atendimento.

RN21 — Continuidade do prazo de resolução
A transferência de um chamado para outro técnico não reiniciará nem prolongará automaticamente o prazo de resolução.
A contagem continuará a partir da atribuição original do chamado, considerando as horas úteis configuradas no sistema.
O sistema deverá preservar o histórico de todas as transferências, incluindo os responsáveis anteriores e as datas das alterações. A transferência não poderá ser utilizada para contornar os limites de prazo definidos para a prioridade do chamado.
Somente se necessário e for autorizado pelo administrador. 

RN22 — Retenção de anexos temporária
Os anexos permanecerão disponíveis durante o atendimento e por sete dias após o encerramento do chamado.
Ao final desse período, o sistema deverá solicitar ao técnico responsável que selecione os arquivos que deseja preservar.

RN23 — Segurança dos anexos
Os anexos deverão respeitar os limites de tamanho, os formatos permitidos e as regras de controle de acesso. A aplicação deverá validar as permissões antes de disponibilizar qualquer arquivo.


## DECISÕES DE ARQUITETURA E TECNOLOGIA
Essa seção apresenta decisões técnicas previstas para orientar a implementação. 

## 8.1. Aplicação
O sistema será desenvolvido como uma aplicação web, inicialmente. 

## 8.2. Backend
A proposta inicial é utilizar Python para o desenvolvimento do backend, integrado com framework Flask. 

## 8.3. Banco de dados
O banco de dados será definido na etapa de modelagem de banco. A proposta é utilizar um banco de dados relacional, o que torna o PostgreSQL uma opção bem forte e a principal.


## 8.4. Interface
A aplicação terá interface responsiva, priorizando a facilidade de uso e clareza de opções, para maior conforto do usuário.

## 8.5. Armazenamento de anexos
Os arquivos serão armazenados fora do banco, durante o desenvolvimento poderá ser utilizado armazenamento local. A solução da produção deverá considerar o controle de acesso, capacidade de armazenamento, cópias de segurança e política de retenção.

## 8.6. Versionamento
O código fonte e a documentação serão mantidos em um repositório Git.

# CONSIDERAÇÕES FINAIS
Esta documentação consolida os requisitos identificados durante o levantamento inicial do sistema.
Antes da modelagem do banco de dados, os requisitos deverão ser revisados para garantir que as funcionalidades principais, as permissões e as regras de negócio estejam suficientemente definidas.
A documentação poderá ser atualizada conforme novas necessidades forem identificadas, mantendo o histórico das decisões relevantes do projeto.

