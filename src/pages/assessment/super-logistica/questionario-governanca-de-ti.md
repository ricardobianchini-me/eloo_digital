---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Governança de TI"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Processos de TI, CMDB e Fornecedores
Cliente: Super Logística | Módulo: Governança de TI
Setor: Logística | Porte: Médio | Interlocutor: Fernanda Costa (Gerente de TI)

> Instrumento de levantamento (Etapa 2 da metodologia), no padrão de rigor de
> working paper (`maturity-scales.md` Seção 5). Toda pergunta declara um Ref
> único (`GOV-{NN}`, contínuo por todo o questionário) e um Método de
> Verificação Exigido — Declarado, Inspecionado ou Testado por amostragem —
> que NÃO é opcional nem decidido pelo entrevistado. Perguntas de percentual
> ou de afirmação sobre uma população de itens (mudanças, ativos, contratos)
> são sempre "Testado por amostragem": a resposta só é válida se trouxer (1)
> população total, (2) amostra efetivamente verificada conforme a Regra de
> Amostragem (≤25 → 100%; 26-100 → mín. 25; 101-500 → mín. 40 ou 10%; >500 →
> mín. 60 ou 8%), e (3) o critério de seleção da amostra. Sem essas três
> informações, o percentual é tratado como evidência insuficiente na Fase 4.
> Esta tabela NÃO contém coluna de Maturidade — a maturidade (0-5) é
> atribuída pelo especialista na Fase 4 (diagnóstico), com base em evidência,
> nunca pelo entrevistado em tempo real.

## Gestão de Incidentes (ITIL 4 — Incident Management)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-01 | Existe ferramenta ou processo formal de registro de incidentes (abertura, categorização, priorização, encerramento)? | Print/acesso à ferramenta de chamados ou planilha de controle com histórico | Inspecionado | | | |
| GOV-02 | Há SLA definido e monitorado para tempo de resposta e resolução por criticidade de incidente? | Documento de SLA formalizado e relatório de acompanhamento de cumprimento de prazos | Inspecionado | | | |
| GOV-03 | Qual o tempo médio de resolução (MTTR) por nível de criticidade (crítico/alto/médio/baixo), com base nos incidentes efetivamente registrados nos últimos 12 meses? | Extração da ferramenta/planilha de incidentes com: (1) população total de incidentes no período por criticidade, (2) amostra verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra, (4) MTTR calculado por criticidade em números reais (não estimativa) | Testado por amostragem | | | |
| GOV-04 | Existe processo de escalonamento formal para incidentes críticos que não são resolvidos dentro do prazo? | Fluxo de escalonamento documentado ou exemplo real de escalonamento aplicado | Inspecionado | | | |
| GOV-05 | A área de TI consegue apresentar histórico/relatório de incidentes dos últimos 12 meses, com volume e categorização? | Relatório ou extração de ferramenta com histórico de incidentes do período | Inspecionado | | | |
| GOV-06 | Incidentes recorrentes ou de alta criticidade geram comunicação formal às áreas de negócio impactadas (ex.: operação logística, roteirização, WMS)? | Exemplo de comunicado ou registro de notificação a stakeholders | Inspecionado | | | |

## Gestão de Problemas (ITIL 4 — Problem Management)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-07 | Existe base de erros conhecidos com causa raiz documentada para incidentes recorrentes? | Base de erros conhecidos (planilha, wiki ou módulo de ferramenta) com casos reais | Inspecionado | | | |
| GOV-08 | Incidentes recorrentes disparam análise formal de causa raiz (RCA), distinta do simples registro do incidente? | Exemplo de RCA documentada para um problema real | Inspecionado | | | |
| GOV-09 | Existe processo de acompanhamento de problemas em aberto até a implementação de solução definitiva (não apenas contorno/workaround)? | Backlog de problemas conhecidos com status de tratativa | Inspecionado | | | |
| GOV-10 | A gestão de problemas está vinculada à gestão de mudanças, de forma que soluções definitivas geram mudanças controladas? | Exemplo de mudança originada de um problema registrado | Inspecionado | | | |

## Gestão de Mudanças (ITIL 4 — Change Enablement)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-11 | Qual o percentual de mudanças implementadas em produção (sistemas, infraestrutura, rede) nos últimos 12 meses que passaram por solicitação formal, avaliação de impacto e aprovação antes da execução? | Extração da ferramenta/planilha de mudanças com: (1) população total de mudanças no período, (2) amostra verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra, (4) percentual resultante de mudanças com aprovação formal | Testado por amostragem | | | |
| GOV-12 | Existe plano de rollback documentado e testado para mudanças classificadas como críticas ou de alto risco? | Template ou exemplo real de plano de rollback | Inspecionado | | | |
| GOV-13 | Existem janelas de mudança definidas para sistemas críticos da operação logística (ex.: WMS, TMS, roteirização)? | Calendário de janelas de mudança ou política formal | Inspecionado | | | |
| GOV-14 | Mudanças emergenciais (fora do fluxo padrão) são registradas retroativamente e revisadas? | Registro de mudanças emergenciais com justificativa e revisão posterior | Inspecionado | | | |
| GOV-15 | Qual a taxa de mudanças emergenciais em relação ao total de mudanças implementadas nos últimos 12 meses? (indicador direto de maturidade de change management — quanto maior a proporção de emergenciais, menor o planejamento prévio) | Extração da ferramenta/planilha de mudanças com: (1) população total de mudanças no período, (2) amostra verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra, (4) percentual de mudanças classificadas como emergenciais vs. planejadas | Testado por amostragem | | | |
| GOV-16 | Existe segregação de funções entre quem solicita, quem aprova e quem executa a mudança? | Matriz de papéis/responsabilidades no processo de mudança | Inspecionado | | | |

## Gestão de Ativos e CMDB (ITIL 4 — IT Asset Management / Service Configuration Management)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-17 | Existe inventário atualizado de ativos de TI (hardware, software, sistemas, itens de configuração) com responsável e localização? | Planilha/ferramenta de inventário atualizada com data da última revisão | Inspecionado | | | |
| GOV-18 | Qual o percentual de ativos do inventário/CMDB efetivamente reconciliados com o ambiente real na última auditoria física/lógica realizada? | Registro da última reconciliação/auditoria de inventário com: (1) população total de ativos cadastrados, (2) amostra verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra, (4) percentual de reconciliação resultante | Testado por amostragem | | | |
| GOV-19 | Existe CMDB formal com relacionamento entre itens de configuração (ex.: qual servidor sustenta qual sistema/aplicação crítica)? | Print/extração da CMDB com relacionamentos mapeados | Inspecionado | | | |
| GOV-20 | Caso não exista CMDB formal, a organização possui outro meio confiável de rastrear dependências entre ativos e sistemas críticos? | Documento alternativo (diagrama, planilha de dependências) atualizado | Inspecionado | | | |
| GOV-21 | Ativos descontinuados/substituídos são baixados formalmente do inventário/CMDB? | Registro de baixa de ativos com data e motivo | Inspecionado | | | |

## Fornecedores e Contratos (COBIT 2019 — APO10 Managed Vendors)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-22 | Existe mapeamento de fornecedores críticos de TI (incluindo fornecedores de sistemas essenciais à operação logística, como WMS/TMS) com classificação de criticidade? | Planilha de fornecedores com criticidade classificada | Inspecionado | | | |
| GOV-23 | Para cada fornecedor crítico identificado, existe plano de contingência formal em caso de descontinuidade, falência ou indisponibilidade do fornecedor? | Documento de plano de contingência por fornecedor crítico | Inspecionado | | | |
| GOV-24 | Qual o percentual de contratos de suporte/SLA vigentes (não vencidos) em relação ao total de contratos ativos com fornecedores de TI? | Lista de contratos com: (1) população total de contratos ativos, (2) amostra verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra, (4) percentual de vigência resultante | Testado por amostragem | | | |
| GOV-25 | Existe algum fornecedor único (ponto único de dependência) sem alternativa de mercado ou plano de migração viável? | Identificação nominal do(s) fornecedor(es) e análise de dependência | Inspecionado | | | |
| GOV-26 | O desempenho de fornecedores críticos (cumprimento de SLA, qualidade de suporte) é avaliado periodicamente? | Relatório de avaliação de fornecedores ou reunião de performance registrada | Inspecionado | | | |

## Documentação de TI e Papéis e Responsabilidades (COBIT 2019 — APO01 Managed I&T Management Framework)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-27 | Existe documentação formal de arquitetura, topologia de rede, sistemas e processos de TI? | Documento(s) de arquitetura/topologia disponível(is) para consulta | Inspecionado | | | |
| GOV-28 | Qual a data da última atualização de cada documento crítico apresentado (arquitetura, processos, políticas)? | Metadados/histórico de versão do documento (data de última revisão) | Inspecionado | | | |
| GOV-29 | Existe política de TI formalizada e comunicada (segurança, uso aceitável, acesso, mudanças)? | Política assinada/publicada e evidência de comunicação aos usuários | Inspecionado | | | |
| GOV-30 | A documentação existente é suficiente para que um novo profissional assuma uma função crítica sem depender do conhecimento tácito de uma pessoa específica? | Runbooks/procedimentos operacionais documentados para funções críticas | Inspecionado | | | |
| GOV-31 | Existe matriz RACI formal e documentada para os principais processos de TI (gestão de incidentes, problemas, mudanças e ativos), definindo quem é Responsável, Aprovador, Consultado e Informado em cada etapa? | Matriz RACI publicada/versionada, cobrindo pelo menos os processos de incidentes, mudanças e ativos | Inspecionado | | | |

## Licenciamento de Software (COBIT 2019 — BAI09 Managed Assets)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-32 | Existe confronto formal entre licenças contratadas, licenças instaladas e licenças efetivamente utilizadas (contratado x instalado x utilizado)? | Relatório de auditoria de licenciamento com as três dimensões comparadas | Inspecionado | | | |
| GOV-33 | Existe processo de auditoria periódica de licenciamento (sistema operacional, banco de dados, aplicações, ferramentas de escritório)? | Registro da última auditoria de licenciamento realizada, com data | Inspecionado | | | |
| GOV-34 | A organização já foi notificada ou auditada por fabricante quanto a uso de software sem licenciamento adequado? | Relato do entrevistado; se aplicável, correspondência ou registro de notificação/auditoria de fabricante | Declarado | | | |
| GOV-35 | Existe controle sobre instalação de software não homologado pelos usuários (shadow IT)? | Política de instalação de software e evidência de controle técnico (ex.: restrição de permissão, allowlist) | Inspecionado | | | |
| GOV-36 | Softwares de sistemas críticos da operação logística (WMS, TMS, roteirização) têm licenciamento formalmente vigente e dimensionado para o volume de uso atual? | Contrato/nota fiscal de licenciamento vigente com quantidade contratada | Inspecionado | | | |

## Políticas de TI (COBIT 2019 — APO01 Managed I&T Management Framework)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-37 | Além da política já mapeada, existem outras políticas formais de TI documentadas e aprovadas pela liderança (ex.: uso aceitável, segurança da informação, classificação de dados, backup, acesso remoto)? Quais existem e quais não? | Lista das políticas vigentes, com data de aprovação e aprovador | Inspecionado | | | |
| GOV-38 | Há quanto tempo cada política vigente foi revisada pela última vez? Existe ciclo formal de revisão periódica? | Registro de datas de revisão por política + processo/periodicidade de revisão | Inspecionado | | | |
| GOV-39 | Qual o percentual de colaboradores que formalmente confirmaram ciência das políticas de TI vigentes (aceite/assinatura)? | Relatório de aceite/assinatura com população total de colaboradores, amostra verificada conforme a Regra de Amostragem e critério de seleção | Testado por amostragem | | | |

## Gestão de Ativos, Hardware e Leasing (ITIL 4 — Asset Management / COBIT 2019 — BAI09 Managed Assets)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| GOV-40 | Qual o percentual de ativos de hardware fisicamente auditados (contagem física) nos últimos 12 meses em relação ao inventário/CMDB registrado? | Relatório de auditoria física com população total de ativos, amostra verificada conforme a Regra de Amostragem e critério de seleção | Testado por amostragem | | | |
| GOV-41 | Quais ativos de TI (hardware ou infraestrutura) estão sob contrato de leasing/arrendamento? Qual o prazo restante e a condição de fim de contrato (devolução, compra, renovação) de cada um? | Lista de contratos de leasing vigentes, com prazo, valor residual e condição de encerramento | Inspecionado | | | |
| GOV-42 | Existe processo formal de baixa/descarte de ativos de TI (hardware) fora de uso, com registro de sanitização de dados antes do descarte? | Processo documentado + registro de baixa/descarte dos últimos ativos desativados | Inspecionado | | | |
