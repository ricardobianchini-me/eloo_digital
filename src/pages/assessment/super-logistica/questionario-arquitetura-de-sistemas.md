---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Arquitetura de Sistemas"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Sistemas, Aplicações e Bancos de Dados
Cliente: Super Logística | Módulo: Arquitetura de Sistemas

> Padrão de rigor de working paper (`maturity-scales.md` Seção 5). Toda
> pergunta classificada como "Testado por amostragem" exige, na resposta:
> (1) população total do item avaliado, (2) tamanho da amostra efetivamente
> verificada, (3) critério de seleção da amostra. Regra de amostragem: ≤25
> itens → testar 100%; 26-100 → mínimo 25; 101-500 → mínimo 40 ou 10% (o
> maior); >500 → mínimo 60 ou 8% (o maior). Percentual sem essas três
> informações = evidência insuficiente = "Não evidenciado" no diagnóstico,
> independentemente do que foi alegado.

## Inventário de Sistemas e Aplicações

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-01 | Quantos sistemas e aplicações estão atualmente em uso na operação (contagem total, incluindo internos, legados, SaaS e de nicho como TMS, WMS, roteirizador, rastreamento de frota)? | Nenhuma evidência documental obrigatória; a resposta define a população-base para dimensionar a amostragem das perguntas seguintes deste subtema | Declarado | | | |
| ARQ-02 | Existe inventário formal e centralizado de todos os sistemas e aplicações em uso? | Planilha ou ferramenta de inventário atualizada | Inspecionado | | | |
| ARQ-03 | Qual o percentual de sistemas do inventário com proprietário de processo (área de negócio) E responsável técnico atribuídos separadamente? | População total de sistemas (ARQ-01), amostra conforme Regra de Amostragem, critério de seleção, e % com ambos os campos preenchidos verificado na amostra | Testado por amostragem | | | |
| ARQ-04 | O inventário é atualizado periodicamente, com data da última revisão registrada? | Histórico de versões do inventário ou log de atualização, com data da última revisão | Inspecionado | | | |
| ARQ-05 | Qual o percentual de sistemas do inventário corretamente classificados quanto à criticidade para a operação (ex.: roteirização, rastreamento, faturamento de fretes sinalizados como críticos)? | População total de sistemas (ARQ-01), amostra conforme Regra de Amostragem, critério de seleção, e % com classificação de criticidade correta verificado na amostra | Testado por amostragem | | | |
| ARQ-06 | Qual o percentual de sistemas do inventário com origem (interno/terceiro/SaaS) e fornecedor corretamente identificados, quando aplicável? | População total de sistemas (ARQ-01), amostra conforme Regra de Amostragem, critério de seleção, e % com origem/fornecedor corretamente preenchidos | Testado por amostragem | | | |
| ARQ-07 | Qual o percentual de sistemas do inventário com dependências entre aplicações mapeadas (diagrama ou matriz de relacionamento)? | População total de sistemas (ARQ-01), amostra conforme Regra de Amostragem, critério de seleção, e % com dependências mapeadas e validadas na amostra | Testado por amostragem | | | |

## Versionamento de Código-Fonte

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-08 | Quantos sistemas foram desenvolvidos ou customizados internamente (in-house)? | Nenhuma evidência documental obrigatória; define a população-base das perguntas de versionamento a seguir | Declarado | | | |
| ARQ-09 | Qual o percentual de sistemas in-house cujo código-fonte está integralmente em repositório versionado (Git ou equivalente)? | População de sistemas in-house (ARQ-08), amostra conforme Regra de Amostragem, critério de seleção, e print do repositório com histórico de commits para cada item amostrado | Testado por amostragem | | | |
| ARQ-10 | O repositório de código possui backup próprio, independente da máquina de qualquer desenvolvedor? | Evidência de configuração de backup/replicação do repositório (print de configuração ou política) | Inspecionado | | | |
| ARQ-11 | Existe política formal de revisão de código (pull request/code review obrigatório) antes de merge/deploy? | Documento de política ou configuração de revisão obrigatória na ferramenta (branch protection, regra de PR) | Inspecionado | | | |
| ARQ-12 | Qual o percentual de merges/pull requests dos últimos 12 meses que efetivamente passaram por revisão obrigatória antes do merge? | População total de merges/PRs no período (extraída da ferramenta), amostra conforme Regra de Amostragem, critério de seleção, e % com revisão registrada antes do merge, verificado na amostra | Testado por amostragem | | | |
| ARQ-13 | Qual o percentual de scripts de integração, automações e customizações (ex.: em roteirizador ou TMS) que também estão versionados, e não apenas o sistema principal? | População de scripts/customizações identificadas, amostra conforme Regra de Amostragem, critério de seleção, e print do repositório contendo os itens amostrados | Testado por amostragem | | | |
| ARQ-14 | Existe controle formal de quem tem acesso de escrita ao repositório e processo definido para revogar esse acesso ao desligar um colaborador? | Política de acesso ao repositório ou procedimento de desligamento com etapa de revogação de acesso a repositório | Inspecionado | | | |
| ARQ-15 | Dos colaboradores com acesso de escrita ao repositório desligados nos últimos 12 meses, qual percentual teve o acesso revogado em até 5 dias úteis? | População total de desligamentos com acesso de escrita no período, amostra conforme Regra de Amostragem, critério de seleção, e log de revogação com datas para os itens amostrados | Testado por amostragem | | | |

## Ambientes Dev/Homolog/Produção

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-16 | Qual o percentual de sistemas críticos com ambientes segregados de desenvolvimento, homologação e produção efetivamente implementados? | População de sistemas críticos (subconjunto de ARQ-01/ARQ-05), amostra conforme Regra de Amostragem, critério de seleção, e documentação de arquitetura de ambientes por sistema amostrado | Testado por amostragem | | | |
| ARQ-17 | Qual o percentual de sistemas com dados de produção mascarados/anonimizados antes de uso em ambiente de homologação ou teste? | População de sistemas com ambiente de homologação, amostra conforme Regra de Amostragem, critério de seleção, e evidência de processo/ferramenta de mascaramento por sistema amostrado | Testado por amostragem | | | |
| ARQ-18 | Existe matriz formal de acesso por ambiente, segregando quem pode acessar desenvolvimento, homologação e produção? | Matriz de acesso por ambiente, documentada e atualizada | Inspecionado | | | |
| ARQ-19 | Dos desenvolvedores/técnicos com acesso a produção, qual percentual tem justificativa formal de necessidade operacional registrada? | População total de contas com acesso a produção, amostra conforme Regra de Amostragem, critério de seleção, e registro de justificativa por conta amostrada | Testado por amostragem | | | |
| ARQ-20 | Qual o percentual de releases dos últimos 12 meses que foram obrigatoriamente testados em homologação antes de ir para produção? | População total de releases no período (log de deployments), amostra conforme Regra de Amostragem, critério de seleção, e checklist/registro de aprovação de homologação por release amostrado | Testado por amostragem | | | |

## Gestão de Mudanças

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-21 | Existe processo formal de gestão de mudanças documentado para alterações em sistemas de produção? | Documento de processo de change management, aprovado e vigente | Inspecionado | | | |
| ARQ-22 | Qual o percentual de mudanças em produção dos últimos 12 meses que passou por aprovação formalmente registrada antes da execução? | População total de mudanças no período (extraída de ticket/log de mudanças), amostra conforme Regra de Amostragem, critério de seleção, e registro/ticket de aprovação por mudança amostrada | Testado por amostragem | | | |
| ARQ-23 | Existe plano de rollback documentado, como parte padrão do processo, para mudanças classificadas como críticas? | Template ou política exigindo plano de rollback documentado para mudanças críticas | Inspecionado | | | |
| ARQ-24 | Qual o percentual de mudanças críticas dos últimos 12 meses que teve plano de rollback formalmente registrado antes da execução? | População total de mudanças críticas no período, amostra conforme Regra de Amostragem, critério de seleção, e plano de rollback registrado por mudança amostrada | Testado por amostragem | | | |
| ARQ-25 | Existe janela de mudança definida e calendarizada para sistemas críticos da operação (ex.: TMS, faturamento), minimizando impacto no negócio? | Calendário ou política de janelas de mudança vigente | Inspecionado | | | |
| ARQ-26 | Qual o percentual de mudanças em produção dos últimos 12 meses rastreáveis até a versão/commit de código que as originou? | População total de mudanças no período, amostra conforme Regra de Amostragem, critério de seleção, e vínculo mudança↔versão/commit por item amostrado | Testado por amostragem | | | |

## Release e Deployment

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-27 | Existe processo padronizado e documentado de release/deployment para publicar novas versões em produção? | Documento de processo de release ou pipeline configurado e documentado | Inspecionado | | | |
| ARQ-28 | Qual o percentual de sistemas críticos com pipeline de deploy automatizado (CI/CD), em vez de execução manual passo a passo? | População de sistemas críticos, amostra conforme Regra de Amostragem, critério de seleção, e evidência de pipeline de CI/CD configurado por sistema amostrado | Testado por amostragem | | | |
| ARQ-29 | Existe checklist ou critério de aceite formal exigido antes de autorizar um deploy em produção? | Checklist de release, vigente e efetivamente utilizado | Inspecionado | | | |
| ARQ-30 | Nos últimos 12 meses, qual foi a taxa de sucesso de deploy vs. rollback, em números absolutos (total de deploys realizados, quantos exigiram rollback, e taxa de sucesso resultante)? | Log de releases/deployments do período com contagem total de deploys e de rollbacks; se a população de deploys registrados for superior a 25, aplicar a Regra de Amostragem sobre os registros individualmente verificados para validar a contagem informada, citando amostra e critério de seleção | Testado por amostragem | | | |
| ARQ-31 | Qual o percentual de deployments dos últimos 12 meses com registro completo no log de releases (data, responsável e versão)? | População total de deployments no período, amostra conforme Regra de Amostragem, critério de seleção, e verificação de completude do registro por item amostrado | Testado por amostragem | | | |

## Atualizações de Sistemas

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-32 | Existe processo formal e periódico de atualização (patches, upgrades) dos sistemas e aplicações em uso? | Cronograma ou política de atualização vigente | Inspecionado | | | |
| ARQ-33 | Qual o percentual de sistemas de terceiros/fornecedores (TMS, WMS, ERP) em versões atualmente suportadas pelo fabricante, sem risco de fim de suporte (end-of-life)? | População total de sistemas de terceiros (ARQ-01), amostra conforme Regra de Amostragem, critério de seleção, e relatório de versão + data de fim de suporte por sistema amostrado | Testado por amostragem | | | |
| ARQ-34 | Existe ambiente de teste dedicado para validar atualizações antes de aplicá-las em produção? | Evidência de ambiente de homologação usado especificamente para teste de atualizações | Inspecionado | | | |
| ARQ-35 | Qual o percentual de sistemas legados sem atualização recente que possui justificativa formal documentada para a não atualização (aceite de risco)? | População de sistemas legados identificados sem atualização recente, amostra conforme Regra de Amostragem, critério de seleção, e registro de exceção/aceite de risco por sistema amostrado | Testado por amostragem | | | |

## Bancos de Dados

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-36 | Existe inventário de todos os bancos de dados em uso, com versão, fabricante e sistema(s) associado(s)? | Inventário de bancos de dados, atualizado | Inspecionado | | | |
| ARQ-37 | Qual o percentual de bancos de dados críticos (ex.: base de fretes, rastreamento, faturamento) com rotina de backup efetivamente testada e validada (teste de restauração)? | População total de bancos de dados críticos, amostra conforme Regra de Amostragem, critério de seleção, e evidência de teste de restauração (data e resultado) por banco amostrado — registrar sobreposição com o domínio de Backup e Continuidade | Testado por amostragem | | | |
| ARQ-38 | Qual o percentual de contas com acesso a bancos de dados de produção cujo nível de acesso é compatível com a função (segregação por perfil, sem acesso direto desnecessário)? | População total de contas com acesso a bancos de produção, amostra conforme Regra de Amostragem, critério de seleção, e matriz de acesso validada por conta amostrada | Testado por amostragem | | | |
| ARQ-39 | Qual o percentual de bancos de dados cujas alterações de schema/estrutura seguem processo controlado e versionado (scripts de migração rastreáveis)? | População total de bancos de dados (ARQ-36), amostra conforme Regra de Amostragem, critério de seleção, e repositório de scripts de migração por banco amostrado | Testado por amostragem | | | |
| ARQ-40 | Existe monitoramento de performance e capacidade dos bancos de dados críticos, com alertas configurados? | Dashboard ou relatório de monitoramento de banco de dados, com evidência de alertas configurados | Inspecionado | | | |

## Integrações e Interfaces

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-41 | Quantas integrações ativas existem atualmente entre sistemas (ex.: TMS-WMS, roteirizador-rastreamento, faturamento-ERP)? | Nenhuma evidência documental obrigatória; define a população-base das perguntas seguintes deste subtema | Declarado | | | |
| ARQ-42 | Qual o percentual de integrações ativas mapeadas em diagrama ou planilha, incluindo direção e frequência? | População total de integrações (ARQ-41), amostra conforme Regra de Amostragem, critério de seleção, e diagrama/planilha validado por integração amostrada | Testado por amostragem | | | |
| ARQ-43 | Qual o percentual de integrações ativas corretamente classificadas por criticidade de dependência para a operação (ex.: integração batch noturna crítica de fretes vs. sincronização cosmética)? | População total de integrações (ARQ-41), amostra conforme Regra de Amostragem, critério de seleção, e matriz de integrações com classificação validada por item amostrado | Testado por amostragem | | | |
| ARQ-44 | Qual o percentual de integrações críticas com monitoramento e alertas configurados para falhas ou atrasos? | População de integrações críticas (subconjunto de ARQ-43), amostra conforme Regra de Amostragem, critério de seleção, e evidência de alerta configurado por integração amostrada | Testado por amostragem | | | |
| ARQ-45 | Qual o percentual de integrações com parceiros externos (transportadoras, clientes, órgãos regulatórios) que possui contrato ou SLA formal definindo responsabilidades? | População de integrações com parceiros externos, amostra conforme Regra de Amostragem, critério de seleção, e contrato/SLA por integração amostrada | Testado por amostragem | | | |
| ARQ-46 | Existe plano de contingência documentado para o caso de indisponibilidade de uma integração crítica (ex.: operação manual temporária)? | Plano de contingência de integração, documentado e vigente | Inspecionado | | | |

## Qualidade, Testes Automatizados e Débito Técnico

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| ARQ-47 | Existe suíte de testes automatizados (unitários e/ou de integração) para os sistemas classificados como críticos? | Evidência de suíte de testes configurada (pipeline, repositório de testes) para pelo menos um sistema crítico | Inspecionado | | | |
| ARQ-48 | Qual a cobertura de testes automatizados (% de código coberto), por sistema crítico, medida por ferramenta de cobertura (não estimativa verbal)? | População de sistemas críticos, amostra conforme Regra de Amostragem se a população for superior a 25, critério de seleção, e relatório de ferramenta de cobertura (ex.: percentual gerado pela pipeline) por sistema amostrado | Testado por amostragem | | | |
| ARQ-49 | Existe registro formal de débito técnico (backlog documentado em ferramenta, e não apenas conhecimento tácito da equipe)? | Ferramenta ou planilha de backlog de débito técnico, ativa e em uso | Inspecionado | | | |
| ARQ-50 | Qual o volume atual do backlog de débito técnico documentado — número total de itens abertos, aging médio (tempo desde a abertura) e os sistemas mais afetados? | Extração direta da ferramenta/planilha de backlog (ARQ-49) com contagem de itens, aging médio calculado e ranking de sistemas por volume de itens — inspeção direta da fonte única de dados, não amostragem sobre uma população de sistemas | Inspecionado | | | |
| ARQ-51 | Existe processo formal de priorização e alocação de tempo/sprint dedicado à redução do débito técnico registrado? | Política de alocação de capacidade (ex.: % de sprint) ou registro de itens de débito técnico efetivamente fechados nos últimos ciclos | Inspecionado | | | |
