---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Backup e Continuidade"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

> **Nota de status:** o interlocutor responsável pelo domínio de Backup/DR ainda não foi indicado pela Super Logística (pendência registrada como status Amber no kickoff formal, 2026-09-14, ver `output/2026-09-14-135322/status-log.md`). Este questionário é o trabalho interno do especialista e pode ser gerado/atualizado normalmente; a fase de entrevista e coleta de respostas deste domínio específico permanece bloqueada até que o cliente indique o responsável.

# Questionário — Backup, Disaster Recovery e Continuidade
Cliente: Super Logística | Módulo: Backup e Continuidade

## Rotina de Backup

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-01 | Que percentual dos sistemas críticos identificados no escopo do assessment (bancos de dados, VMs, código-fonte, configurações de rede/segurança) possui rotina de backup configurada? | População total de sistemas críticos do escopo, tamanho da amostra efetivamente verificada na ferramenta de backup e critério de seleção da amostra (Regra de Amostragem — ver `maturity-scales.md` Seção 5.3: ≤25 itens = 100%; 26-100 = mín. 25; 101-500 = mín. 40 ou 10%; >500 = mín. 60 ou 8%). Percentual sem essas três informações é evidência insuficiente. | Testado por amostragem | | | |
| BKP-02 | Qual a frequência e a janela de execução do backup para cada sistema crítico amostrado? | Configuração de agendamento (política de job) da ferramenta de backup, para os itens da amostra do BKP-01 | Inspecionado | | | |
| BKP-03 | Existe monitoramento ativo de falhas de execução do backup, com alerta e ação corretiva registrada? | Log/relatório de execução com histórico de sucesso/falha e evidência de tratativa | Inspecionado | | | |
| BKP-04 | Qual foi a data e o resultado da última falha de backup identificada, e qual foi a ação tomada? | Registro de incidente/chamado referente à falha, com data de abertura e de resolução | Inspecionado | | | |
| BKP-05 | O código-fonte dos sistemas próprios e as configurações críticas de rede/segurança estão incluídos no escopo de backup, além de bancos de dados e VMs? | Evidência de job de backup cobrindo repositórios de código e configurações (ex.: export de config de firewall/switch), com data do último job executado | Inspecionado | | | |

## Teste de Restauração

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-06 | Que percentual dos sistemas críticos do escopo teve teste de restauração completo comprovado nos últimos 12 meses? | População total de sistemas críticos, amostra efetivamente verificada e critério de seleção (Regra de Amostragem, Seção 5.3). Percentual "de cabeça" sem essas três informações não é aceito. | Testado por amostragem | | | |
| BKP-07 | Qual foi a data, o escopo e o resultado do último teste de restauração completo documentado, individualmente por sistema crítico amostrado no BKP-06? | Relatório de teste de restauração com data, escopo e resultado, por sistema | Inspecionado | | | |
| BKP-08 | Os testes de restauração são realizados em periodicidade definida (ex.: trimestral) e essa periodicidade é cumprida? | Calendário/política de testes de restauração e histórico de execução dos últimos 4 ciclos | Inspecionado | | | |
| BKP-09 | Quem executou e quem validou o resultado do último teste de restauração de cada sistema amostrado? | Registro nominal de executor e validador no relatório de teste | Inspecionado | | | |
| BKP-10 | Qual foi o tempo real medido (em horas/minutos) para concluir o último teste de restauração de cada sistema crítico, comparado ao RTO prometido para aquele sistema? | Relatório de teste com timestamp de início/fim da restauração, cruzado com a tabela de RTO por serviço (ver BKP-22); gap quantificado em horas ou percentual, não apenas "dentro do esperado" | Inspecionado | | | |
| BKP-11 | Já houve tentativa de restauração que falhou ou revelou dados corrompidos/incompletos? Qual foi o resultado e a correção aplicada? | Registro de incidente de restauração malsucedida e plano de correção, com data de identificação e de fechamento | Inspecionado | | | |

## Cópia Externa e Proteção Antiransomware

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-12 | Existe cópia externa/off-site ou em nuvem, segregada logicamente e fisicamente do ambiente de produção? | Print de configuração de replicação externa mostrando segregação de rede/credenciais | Inspecionado | | | |
| BKP-13 | Quando foi o último teste de acesso/integridade realizado sobre a cópia externa, e qual foi o resultado? | Relatório de verificação de integridade da cópia externa com data e resultado | Inspecionado | | | |
| BKP-14 | Há proteção específica contra ransomware nas cópias de backup, como imutabilidade (WORM) ou air-gap? | Documentação técnica da funcionalidade ativada (ex.: configuração de retenção imutável, print do console) | Inspecionado | | | |
| BKP-15 | As credenciais de acesso ao sistema de backup são distintas das credenciais de administração do ambiente de produção? | Evidência de conta/segregação de acesso dedicada ao backup (ex.: print de grupo de acesso ou IAM policy) | Inspecionado | | | |
| BKP-16 | Quem tem acesso físico e/ou lógico à cópia externa (custódia da mídia/credenciais), e essa cadeia de custódia é documentada e revisada periodicamente? | Lista nominal de pessoas/perfis com acesso físico (cofre, datacenter, mídia removível) e lógico (credenciais/chaves de acesso à cópia externa), com data da última revisão de acesso | Inspecionado | | | |
| BKP-17 | Em caso de comprometimento (ex.: ransomware) do ambiente de produção, a cópia externa está isolada de forma que as credenciais comprometidas não alcancem também a cópia de backup? | Diagrama ou documentação técnica de segregação de domínio/rede entre produção e a camada de backup externo | Inspecionado | | | |

## Retenção

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-18 | Qual é a política de retenção de backup definida por sistema, e ela está documentada formalmente? | Documento de política de retenção com prazos por sistema, versionado | Inspecionado | | | |
| BKP-19 | A retenção definida atende requisitos regulatórios ou contratuais aplicáveis ao setor de logística (ex.: fiscais, trabalhistas, contratos com embarcadores)? | Mapeamento de requisito legal/contratual x prazo de retenção configurado, por sistema | Inspecionado | | | |
| BKP-20 | Quando foi a última verificação de que os backups mais antigos dentro do prazo de retenção ainda são recuperáveis? | Relatório de teste de restauração sobre backup de retenção longa, com data e resultado | Inspecionado | | | |

## Plano de Disaster Recovery

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-21 | Existe plano de Disaster Recovery documentado e formalmente aprovado? | Documento do plano de DR com data de aprovação e responsável nomeado | Inspecionado | | | |
| BKP-22 | O plano de DR cobre todos os sistemas críticos identificados no escopo do assessment, incluindo dependências entre sistemas? | Mapeamento de sistemas críticos x cobertura do plano de DR, incluindo diagrama de dependências | Inspecionado | | | |
| BKP-23 | Quando o plano de DR foi revisado pela última vez e o que mudou desde então no ambiente de produção? | Histórico de versões do documento do plano de DR, com changelog | Inspecionado | | | |
| BKP-24 | Existe site/ambiente de contingência definido (próprio, contratado ou em nuvem) para execução do plano de DR? | Contrato ou configuração de ambiente de contingência, com evidência de disponibilidade atual | Inspecionado | | | |
| BKP-25 | Qual seria o custo estimado (financeiro e de tempo de equipe) de um cenário de recuperação total simulado, e esse cenário já foi de fato executado como simulação? | Relatório de simulação de recuperação total (tabletop ou execução real) com estimativa de custo/esforço e data de realização; se nunca simulado, registrar explicitamente a ausência | Inspecionado | | | |

## RTO/RPO

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-26 | RTO (tempo máximo de indisponibilidade aceitável) está definido individualmente para cada serviço crítico? | Tabela de RTO por serviço, aprovada pela área de negócio | Inspecionado | | | |
| BKP-27 | RPO (perda máxima de dados aceitável) está definido individualmente para cada serviço crítico? | Tabela de RPO por serviço, aprovada pela área de negócio | Inspecionado | | | |
| BKP-28 | O RTO e o RPO definidos foram efetivamente alcançados no último teste de DR realizado, com medição registrada por serviço? | Relatório de teste de DR com tempo de recuperação e ponto de dados recuperado medidos, por serviço, cruzado com a tabela de metas (BKP-26/BKP-27) | Inspecionado | | | |
| BKP-29 | Existe alguma diferença (gap) entre o RTO/RPO formalmente definido e a capacidade real observada em testes? Qual é o tamanho desse gap, em horas/minutos, e como está sendo tratado? | Comparativo quantificado entre meta definida e resultado medido, com plano de ação e prazo para a lacuna | Inspecionado | | | |

## Testes de Continuidade

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| BKP-30 | O plano de DR foi testado nos últimos 12 meses, com resultado registrado? | Relatório de teste de DR/continuidade com data e escopo testado | Inspecionado | | | |
| BKP-31 | Os testes de continuidade envolvem simulação de cenário real (ex.: indisponibilidade de datacenter, ataque de ransomware) ou apenas checklist documental? | Roteiro/metodologia do teste realizado, indicando se foi simulação funcional ou revisão de documento | Inspecionado | | | |
| BKP-32 | Quais lacunas foram identificadas no último teste de continuidade e qual o status do plano de correção? | Relatório de teste com lista de não conformidades e plano de ação associado, com prazos e responsáveis | Inspecionado | | | |
| BKP-33 | O conhecimento necessário para executar a recuperação (backup e DR) está documentado em procedimento escrito e replicável, ou está concentrado em uma pessoa específica? | Procedimento de recuperação escrito, com matriz de responsáveis e plano de sucessão/backup de pessoal | Inspecionado | | | |
| BKP-34 | Existe plano de comunicação definido (interno e com clientes/parceiros/embarcadores) para cenários de indisponibilidade prolongada? | Documento de plano de comunicação de crise/continuidade, com canais e responsáveis definidos | Inspecionado | | | |
