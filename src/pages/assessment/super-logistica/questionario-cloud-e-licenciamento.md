---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Cloud e Licenciamento"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Ativos e Licenciamento em Nuvem
Cliente: Super Logística | Módulo: Cloud e Licenciamento
Interlocutor de referência: Bruno Alves, Coordenador de Infraestrutura (acumula Cloud)

> Padrão de rigor de working paper (`pipeline/data/maturity-scales.md` Seção 5): toda pergunta tem um Ref sequencial contínuo (`CLD-NN`) e um Método de Verificação Exigido — Declarado, Inspecionado ou Testado por amostragem. Este questionário NÃO contém coluna de Maturidade: a maturidade é atribuída pelo especialista na Fase 4 (diagnóstico), sempre com base em evidência, nunca em declaração isolada do entrevistado. Toda pergunta "Testado por amostragem" exige, na resposta, população total + amostra efetivamente verificada + critério de seleção (Regra de Amostragem, Seção 5.3) — sem isso, o item é tratado como "Não evidenciado" no diagnóstico, independentemente do percentual alegado.

## Inventário de Recursos Cloud

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| CLD-01 | Quais provedores de nuvem são utilizados (IaaS/PaaS/SaaS) e para quais finalidades? | Lista de provedores contratados com escopo de uso de cada um | Declarado | | | |
| CLD-02 | Existe inventário consolidado de todos os recursos provisionados em nuvem, com dono e propósito identificados? | Export do inventário/tags do(s) provedor(es) ou ferramenta de CMDB cloud | Inspecionado | | | |
| CLD-03 | Qual o percentual de recursos provisionados com tag de dono, projeto ou centro de custo corretamente atribuída (recursos não órfãos)? | Relatório de tagging do console do provedor, informando população total de recursos, amostra efetivamente verificada e critério de seleção (Regra de Amostragem, Seção 5.3) | Testado por amostragem | | | |
| CLD-04 | Existe uma política de tagging obrigatório formalmente definida (nomenclatura padrão, campos obrigatórios, responsáveis)? | Documento de política de tagging | Inspecionado | | | |
| CLD-05 | Essa política de tagging é tecnicamente enforçada — isto é, existe controle automatizado (ex.: policy-as-code, Service Control Policies, Azure Policy, Tag Policies, Organization Policies) que bloqueia ou sinaliza a criação de recursos sem tag obrigatória — ou depende apenas de processo manual/orientação sem bloqueio técnico? | Print/export da configuração do mecanismo de enforcement técnico (regra ativa e escopo de aplicação); na ausência, declaração explícita de que o controle é apenas processual | Inspecionado | | | |
| CLD-06 | Existe processo formal de provisionamento e desprovisionamento de recursos (criação e desligamento)? | Procedimento documentado de provisionamento/decomissionamento | Inspecionado | | | |
| CLD-07 | Em ambiente com múltiplos provedores, contas ou assinaturas, existe visão unificada do inventário, ou cada uma é controlada separadamente? | Ferramenta de inventário multi-cloud/multi-conta ou planilha consolidada mantida ativamente, com data da última atualização | Inspecionado | | | |
| CLD-08 | Dos recursos identificados como obsoletos ou não utilizados (idle) na última revisão periódica, qual o percentual que foi efetivamente desligado ou ajustado nos últimos 12 meses? | Registro de revisões periódicas (data, responsável, recursos identificados) com população total de recursos idle identificados, amostra/total verificado da ação tomada e critério de seleção | Testado por amostragem | | | |

## Governança de Custo (FinOps)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| CLD-09 | Existe acompanhamento mensal de custo por serviço, projeto ou centro de custo? | Relatório de billing segmentado (dashboard FinOps ou planilha de custo) dos últimos 3 meses | Inspecionado | | | |
| CLD-10 | Em ambiente com múltiplas contas/assinaturas/projetos, existe processo formal de reconciliação de billing consolidado — isto é, conciliação entre o valor total cobrado pelo provedor (fatura consolidadora) e o custo alocado a cada centro de custo/projeto internamente? | Procedimento documentado de reconciliação de billing multi-conta/multi-assinatura, com evidência de execução no último ciclo de faturamento | Inspecionado | | | |
| CLD-11 | Qual o percentual de contas/assinaturas cloud ativas na organização que estão de fato incluídas no agrupamento de faturamento consolidado e no processo de reconciliação (vs. contas "órfãs", fora do agrupamento oficial de billing)? | Relatório de contas/assinaturas do provedor (ex.: AWS Organizations, Azure EA/MCA, GCP Billing Account) confrontado com a lista de contas incluídas na reconciliação, informando população total de contas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-12 | Alertas de orçamento (budget alerts) estão configurados para consumo anormal ou acima do previsto? | Print de configuração de budget alert/threshold no console do provedor | Inspecionado | | | |
| CLD-13 | Houve, nos últimos 12 meses, variação relevante de custo (para cima) sem explicação de capacidade/negócio associada? | Histórico de billing dos últimos 12 meses com nota de justificativa técnica das variações relevantes | Inspecionado | | | |
| CLD-14 | Existe responsável formal (pessoa ou área) por aprovar e justificar novos gastos em nuvem? | Política de aprovação de provisionamento com identificação do aprovador | Inspecionado | | | |
| CLD-15 | Dos recursos identificados como superprovisionados (dimensionados acima da necessidade real) na última análise de rightsizing, qual o percentual efetivamente ajustado? | Relatório de rightsizing/otimização de custo com população total de recursos superprovisionados identificados, amostra/total verificado quanto ao ajuste efetuado e critério de seleção | Testado por amostragem | | | |
| CLD-16 | Qual a cobertura de reservas, planos de economia ou descontos por compromisso (reserved instances/savings plans) sobre as cargas de trabalho elegíveis a esse tipo de desconto? | Relatório de cobertura de reservas vs. uso sob demanda, com população total de cargas elegíveis, amostra/total verificado e critério de seleção | Testado por amostragem | | | |

## Controle de Acesso e Privilégios

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| CLD-17 | Existe política de controle de acesso (IAM) formalizada para os ambientes em nuvem? | Documento de política de IAM/RBAC | Inspecionado | | | |
| CLD-18 | Qual o percentual de contas de usuário humano com acesso administrativo que seguem o princípio de privilégio mínimo (acesso restrito ao necessário para a função, sem permissões amplas desnecessárias)? | Matriz de papéis e permissões (roles) configurada no provedor, confrontada com a necessidade funcional de cada conta, informando população total de contas administrativas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-19 | Qual o percentual de contas de serviço e chaves de API inventariadas e auditadas nos últimos 12 meses quanto a dono, escopo de permissão e necessidade — com o mesmo rigor aplicado a contas humanas? | Lista de service accounts/API keys com dono, escopo de permissão e data da última auditoria, informando população total, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-20 | Existem roles ou políticas de permissão CUSTOMIZADAS (criadas pela própria equipe de TI, distintas dos papéis/roles nativos e pré-definidos do provedor) em uso no ambiente cloud? | Export de roles/políticas do provedor com marcação de origem (nativa vs. customizada) | Inspecionado | | | |
| CLD-21 | Existe processo formal de revisão periódica de least-privilege aplicado especificamente às roles customizadas — e não apenas aos papéis nativos do provedor, que costumam ter revisão facilitada pelo próprio console? | Procedimento documentado de revisão de least-privilege com escopo explícito sobre roles customizadas e evidência de execução do último ciclo | Inspecionado | | | |
| CLD-22 | Das roles customizadas existentes no ambiente, qual o percentual revisado nos últimos 12 meses quanto a permissões excessivas (ex.: uso de wildcard "*" em ações ou recursos, permissões de escrita/exclusão não necessárias)? | Relatório de revisão de roles customizadas com população total de roles customizadas existentes, amostra efetivamente revisada e critério de seleção | Testado por amostragem | | | |
| CLD-23 | Qual o percentual de contas com privilégio de administrador global que possuem justificativa de necessidade formalmente documentada? | Relatório de contas com permissão administrativa confrontado com registro de justificativa, informando população total de contas administrativas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-24 | Qual o percentual de contas com acesso administrativo aos consoles de nuvem que possuem autenticação multifator (MFA) obrigatória e efetivamente ativa (não apenas disponível/opcional)? | Relatório de status de MFA por conta extraído do provedor de identidade, informando população total de contas administrativas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-25 | Qual o percentual de chaves de API/credenciais de acesso programático ativas há mais de 90 dias sem rotação? | Registro/relatório de rotação de credenciais com data da última execução por chave, informando população total de chaves ativas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-26 | Qual o percentual de acessos de terceiros (integradores, fornecedores) aos ambientes de nuvem revisados nos últimos 12 meses? | Lista de acessos de terceiros com data de concessão e última revisão, informando população total de acessos de terceiros, amostra verificada e critério de seleção | Testado por amostragem | | | |

## Licenciamento SaaS/PaaS

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| CLD-27 | Existe inventário de todos os contratos SaaS/PaaS ativos, com número de licenças contratadas e modelo de cobrança (por usuário ou por consumo)? | Planilha ou sistema de gestão de contratos SaaS/PaaS | Inspecionado | | | |
| CLD-28 | Qual o percentual de contratos SaaS/PaaS ativos com auditoria de uso real realizada nos últimos 12 meses (comparando licenças pagas vs. usuários ativos)? | Relatório de uso ativo vs. licenças pagas (ex.: relatório de login/atividade do provedor), informando população total de contratos ativos, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-29 | Qual o percentual de licenças SaaS/PaaS contratadas identificadas como ociosas ou subutilizadas nos últimos 12 meses? | Relatório de licenças ociosas com respectiva ação de ajuste (cancelamento/redução), informando população total de licenças contratadas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-30 | Existe processo de revisão de contratos SaaS/PaaS antes da renovação automática (avaliação de necessidade e custo)? | Calendário de renovações com checkpoints de revisão antecipada | Inspecionado | | | |
| CLD-31 | Dos contratos SaaS ativos atualmente na organização, qual o percentual foi identificado como contratado por área de negócio sem validação prévia da TI (shadow IT)? | Comparativo entre inventário de contratos SaaS e registro de aprovações de TI, informando população total de contratos ativos, amostra verificada e critério de seleção | Testado por amostragem | | | |

## Continuidade de Recursos Cloud (interface com Breno Backup)

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| CLD-32 | Qual o percentual de recursos críticos em nuvem (bancos de dados, storage, máquinas virtuais) com rotina de backup configurada e ativa nativamente no provedor? | Configuração de backup automatizado do provedor (política/schedule) confrontada com a lista de recursos classificados como críticos, informando população total, amostra verificada e critério de seleção | Testado por amostragem | | | |
| CLD-33 | Qual o percentual de testes de restauração de backup planejados nos últimos 12 meses que foram efetivamente realizados, com registro de resultado? | Registro de testes de restore com data e resultado, informando população total de testes planejados, amostra/total verificado e critério de seleção | Testado por amostragem | | | |
| CLD-34 | Em caso de indisponibilidade de uma região/zona do provedor, existe plano de continuidade definido para os recursos hospedados em nuvem? | Plano de continuidade/DR documentado com escopo de recursos cloud | Inspecionado | | | |

## Notas do Especialista

- Este questionário cobre 5 subtemas — Inventário de Recursos Cloud, Governança de Custo/FinOps, Controle de Acesso e Privilégios, Licenciamento SaaS/PaaS e Continuidade de Recursos Cloud — com foco em governança do que já está contratado. Nenhuma pergunta ou recomendação decorrente deste levantamento deve sugerir troca de provedor de nuvem.
- Refs sequenciais contínuos `CLD-01` a `CLD-34`, sem reinício por subtema, conforme `pipeline/data/maturity-scales.md` Seção 5.1. Este Ref é o elo obrigatório entre este questionário (Fase 3) e o diagnóstico de domínio (Fase 4) — todo achado no diagnóstico deve citar o Ref de origem.
- Distribuição por Método de Verificação: 1 pergunta "Declarado" (CLD-01, puramente contextual), 12 perguntas "Inspecionado" (artefato estático único — política, print, procedimento) e 21 perguntas "Testado por amostragem" (toda pergunta de percentual/cobertura/população de recursos, contas, chaves, roles, licenças ou contratos). Nenhum controle crítico (privilégio administrativo, MFA, tagging técnico, roles customizadas, licenciamento ocioso) foi classificado como "Declarado".
- Toda pergunta "Testado por amostragem" exige, na coluna "Resposta do Entrevistado", os três elementos da Regra de Amostragem (Seção 5.3): população total, amostra efetivamente verificada e critério de seleção (aleatória, todos os críticos, por unidade/site/conta). A ausência de qualquer um dos três torna o item "Não evidenciado" no diagnóstico (Fase 4), independentemente do percentual declarado.
- O subtema "Continuidade de Recursos Cloud" tem sobreposição intencional com o domínio de Breno Backup; na consolidação (Fase 4), evitar duplicidade de achados entre os dois especialistas — citar o Ref de origem ajuda a rastrear e evitar essa duplicidade.
- A Maturidade (0-5) NÃO é capturada neste questionário. Ela é atribuída pelo especialista na Fase 4 (`domain-diagnosis-caio-cloud.md`), com base em evidência concreta (documento, print de console, relatório de amostragem), conforme a Escala de Maturidade 0-5 e a Escala de Classificação de Controle (`pipeline/data/maturity-scales.md`, Seções 1 e 3).
