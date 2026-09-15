---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Segurança da Informação"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Segurança da Informação
Cliente: Super Logística | Módulo: Segurança da Informação
Interlocutor(a): Fernanda Costa, Gerente de TI (acumula a frente de Segurança)

> Método de Verificação Exigido, por pergunta: **Declarado** (registro da resposta verbal, nunca suficiente isoladamente para classificar um controle como Adequado) · **Inspecionado** (documento/print/log/configuração pontual revisado durante ou logo após a entrevista) · **Testado por amostragem** (aplica-se a toda pergunta sobre percentual, cobertura de frota ou população de itens; Regra de Amostragem: população ≤25 → testar 100%; 26-100 → amostra mínima de 25; 101-500 → amostra mínima de 40 ou 10% da população, o que for maior; >500 → amostra mínima de 60 ou 8% da população, o que for maior). Toda pergunta "Testado por amostragem" exige, na resposta: (1) população total, (2) tamanho da amostra efetivamente verificada, (3) critério de seleção da amostra. Faltando qualquer um dos três, o diagnóstico classifica automaticamente o controle como "Não evidenciado", independentemente do percentual alegado.
>
> A coluna "Maturidade" NÃO existe neste questionário — a atribuição de maturidade (0-5) é determinação do especialista na Fase 4 (diagnóstico), com base em evidência, nunca capturada durante a entrevista.

## EDR e Antivírus

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| SEG-01 | Qual o percentual real de máquinas (servidores + endpoints) com agente EDR/antivírus ativo e atualizado, extraído do console centralizado? | Relatório do console de gestão informando: (1) população total de ativos (servidores + endpoints), (2) amostra efetivamente verificada conforme a Regra de Amostragem, (3) critério de seleção da amostra (ex.: aleatória, por site, todos os críticos) | Testado por amostragem | | | |
| SEG-02 | Dos servidores (produção, homologação, infraestrutura crítica), qual o percentual coberto por EDR, apurado separadamente da frota de estações de trabalho? | Relatório do console segmentado por classe de ativo, com população total de servidores, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-03 | Existe console centralizado de gestão de EDR/antivírus com visibilidade sobre toda a frota? | Print do console mostrando inventário de endpoints geridos | Inspecionado | | | |
| SEG-04 | Há alertas de detecção configurados e um fluxo definido de resposta a incidentes de endpoint? | Print de política de alertas + documento/fluxo de resposta a incidentes | Inspecionado | | | |
| SEG-05 | Existem máquinas (servidores, notebooks, estações) sem qualquer agente de proteção instalado? Se sim, quais e por quê? | Lista de exceções documentadas com justificativa e plano de regularização | Inspecionado | | | |
| SEG-06 | Existe processo formal de aprovação, prazo de validade e revisão periódica para exceções de proteção de endpoint (máquinas sem EDR)? | Documento de processo de exceções + registro de aprovação/revisão da(s) exceção(ões) vigente(s) | Inspecionado | | | |
| SEG-07 | Com que frequência as assinaturas/definições de ameaças são atualizadas, e qual o percentual da frota em conformidade com essa frequência no momento da verificação? | Relatório de status de atualização por máquina, com população total, amostra verificada e critério de seleção conforme a Regra de Amostragem | Testado por amostragem | | | |
| SEG-08 | Existe segmentação ou isolamento automático de máquina comprometida detectada pelo EDR? | Demonstração de política de isolamento/quarentena no console | Inspecionado | | | |
| SEG-09 | Quem tem acesso ao console de gestão do EDR/antivírus, e esse acesso é revisado periodicamente? | Lista de usuários com acesso ao console + evidência de revisão | Inspecionado | | | |
| SEG-10 | Os endpoints que operam fora da rede corporativa (notebooks remotos, BYOD) recebem o mesmo percentual de cobertura de EDR que os endpoints internos? | Relatório comparativo (interno vs. remoto) com população total de cada grupo, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-11 | Existe SLA definido para tempo de resposta a alertas críticos gerados pelo EDR, e qual foi o tempo médio real de resposta nos últimos 3 meses? | Relatório de alertas críticos do período com população total de alertas críticos, amostra verificada e critério de seleção | Testado por amostragem | | | |

## Identidade e Gestão de Acessos

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| SEG-12 | Todas as contas de ex-colaboradores dos últimos 12 meses foram desativadas? Solicitar lista de desligamentos do RH cruzada com lista de contas ativas no AD/IAM. | Lista de desligamentos (RH) cruzada ativamente com exportação de contas ativas no AD/IAM/sistemas críticos, informando população total de desligados no período, amostra verificada (100% se ≤25, senão conforme a Regra de Amostragem) e critério de seleção — não é aceita apenas declaração verbal | Testado por amostragem | | | |
| SEG-13 | Qual o percentual de contas administrativas (AD, e-mail, VPN, cloud, sistemas críticos) com MFA efetivamente habilitado, verificado diretamente na configuração de cada sistema? | Print de configuração de MFA por conta/sistema, com população total de contas administrativas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-14 | Qual o percentual de contas de usuário comum com MFA habilitado em acessos remotos (VPN, e-mail externo, VDI)? | Print de política de MFA aplicada a acesso remoto, com população total de contas com acesso remoto, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-15 | Existe processo formal de onboarding/offboarding de identidade com checklist de provisionamento e desprovisionamento de acesso? | Documento de processo + evidência de execução recente (chamado/ticket) | Inspecionado | | | |
| SEG-16 | Existe revisão periódica (recertificação) de acessos concedidos? Qual o percentual de colaboradores com acesso a sistemas críticos que foi efetivamente recertificado nos últimos 12 meses? | Relatório da última recertificação de acessos, com população total de colaboradores com acesso a sistemas críticos, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-17 | Existem contas genéricas ou compartilhadas (ex.: "admin", "ti", "financeiro") em uso, e se sim, por quantas pessoas cada uma é utilizada? | Lista de contas genéricas identificadas + confirmação de quantidade de usuários reais por conta | Inspecionado | | | |
| SEG-18 | A política de senhas (complexidade, expiração, histórico) é aplicada tecnicamente (via GPO/IAM) ou apenas orientada por documento? | Print de política técnica configurada no AD/IAM | Inspecionado | | | |
| SEG-19 | Existe diretório único de identidade (AD/Azure AD/IAM) ou os acessos são geridos de forma fragmentada por sistema? | Diagrama/lista de sistemas indicando quais estão integrados ao diretório central (SSO) | Inspecionado | | | |
| SEG-20 | Quantas contas de prestadores de serviço/terceiros com acesso remoto existem atualmente, e qual percentual possui prazo de expiração automático configurado? | Lista de contas de terceiros com população total, amostra verificada e critério de seleção, informando quantas têm expiração automática configurada | Testado por amostragem | | | |
| SEG-21 | Existe processo formal de gestão de exceções à política de senha/MFA (ex.: contas de serviço, sistemas legados incompatíveis), com registro, aprovação, prazo de validade e revisão periódica? | Documento de processo de exceções + registro das exceções vigentes com data de aprovação e próxima revisão | Inspecionado | | | |
| SEG-22 | Existe processo de revisão específica de acessos privilegiados de administradores de rede/servidores/cloud, separado da recertificação geral de usuários comuns? | Documento de processo + evidência da última revisão de acessos privilegiados | Inspecionado | | | |

## Credenciais Privilegiadas

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| SEG-23 | Existem senhas administrativas compartilhadas entre múltiplas pessoas (servidores, banco de dados, rede, cloud)? Solicitar confirmação acompanhada de inspeção das contas genéricas. | Inspeção acompanhada das contas administrativas + confirmação de quantas pessoas conhecem cada senha | Inspecionado | | | |
| SEG-24 | Existe cofre de senhas (PAM/vault) para credenciais privilegiadas, ou as senhas são armazenadas em planilha/documento/memória? | Print do cofre de senhas em uso, ou confirmação documentada da ausência | Inspecionado | | | |
| SEG-25 | Qual o percentual de contas privilegiadas (admin de domínio, servidores, rede, cloud) atualmente cadastradas e geridas dentro do cofre de senhas (PAM), sobre o total de contas privilegiadas identificadas? | Relatório do PAM com população total de contas privilegiadas identificadas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-26 | A mesma pessoa que aprova uma mudança crítica também é quem a executa tecnicamente (ausência de segregação de funções)? | Matriz de quem aprova x quem executa mudanças críticas em sistemas/infraestrutura | Inspecionado | | | |
| SEG-27 | Existe trilha de auditoria de uso de credenciais privilegiadas (quem acessou, quando, o que foi feito)? | Print de log de sessão privilegiada ou de auditoria do PAM/sistema | Inspecionado | | | |
| SEG-28 | Existe MFA habilitado especificamente para acesso ao cofre de senhas (PAM) e para sessões privilegiadas (jump host/bastion)? | Print de configuração de MFA no PAM/bastion | Inspecionado | | | |
| SEG-29 | As senhas administrativas padrão de fábrica (equipamentos de rede, servidores, sistemas) foram alteradas? | Confirmação acompanhada de inspeção de amostra de equipamentos/sistemas, informando população total de equipamentos, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-30 | Qual o percentual de contas de serviço (usadas por aplicações/integrações) com senha rotacionada nos últimos 90 dias, sobre o total de contas de serviço identificadas? | Relatório/política de rotação com população total de contas de serviço, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-31 | Existe monitoramento/alerta em tempo real para uso de credenciais privilegiadas fora do horário comercial ou de localização incomum? | Print de regra de alerta configurada no PAM/SIEM | Inspecionado | | | |
| SEG-32 | Em caso de saída de um administrador de TI, existe processo de troca imediata de todas as credenciais privilegiadas que essa pessoa conhecia? | Documento de processo + evidência de execução no último desligamento de perfil técnico | Inspecionado | | | |

## Segurança de Aplicações

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| SEG-33 | As aplicações críticas de negócio possuem trilha de auditoria de ações realizadas por usuários administrativos (quem fez o quê e quando)? | Print de log de auditoria da(s) aplicação(ões) crítica(s) | Inspecionado | | | |
| SEG-34 | O controle de acesso dentro das aplicações críticas segue perfis de permissão por função (RBAC), ou os usuários têm acesso amplo por padrão? | Print de matriz de perfis/permissões configurada na aplicação | Inspecionado | | | |
| SEG-35 | Qual a data do último teste de penetração (pentest) externo, qual o escopo (quantidade e identificação de aplicações/IPs testados) e qual a frequência contratada (anual, semestral, etc.)? | Relatório do último pentest com data, escopo detalhado e contrato/SoW indicando frequência contratada | Inspecionado | | | |
| SEG-36 | O escopo do último pentest cobriu 100% das aplicações expostas externamente? Se não, qual a população total de aplicações expostas e qual a amostra efetivamente testada? | Relatório de escopo do pentest com população total de aplicações expostas, amostra testada e critério de seleção conforme a Regra de Amostragem | Testado por amostragem | | | |
| SEG-37 | Das vulnerabilidades classificadas como Críticas/Altas no último pentest ou scan, qual o percentual remediado dentro do SLA definido, sobre o total de vulnerabilidades Críticas/Altas identificadas? | Relatório de acompanhamento de remediação com população total de vulnerabilidades Críticas/Altas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-38 | Aplicações que armazenam dados sensíveis (financeiros, pessoais, operacionais críticos) utilizam criptografia em trânsito e em repouso? | Print de configuração de TLS/criptografia de banco de dados | Inspecionado | | | |
| SEG-39 | Existe ambiente de homologação segregado do ambiente de produção para testes antes de liberar mudanças em aplicações críticas? | Diagrama/inventário de ambientes (dev/homologação/produção) | Inspecionado | | | |
| SEG-40 | As credenciais de acesso a bancos de dados e APIs das aplicações críticas são armazenadas em texto claro no código-fonte ou em arquivo de configuração acessível? | Inspeção acompanhada de arquivo de configuração/variáveis de ambiente | Inspecionado | | | |
| SEG-41 | Existe WAF (Web Application Firewall) ativo protegendo as aplicações expostas externamente, com conjunto de regras atualizado? | Print de painel do WAF mostrando regras ativas e data da última atualização | Inspecionado | | | |
| SEG-42 | Qual o percentual de aplicações críticas cujo pipeline de CI/CD inclui verificação de segurança automatizada (SAST/DAST/SCA) antes do deploy em produção? | Relatório/configuração de pipeline com população total de aplicações críticas, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-43 | Existe processo formal de gestão de vulnerabilidades e aplicação de correções (patch) nas aplicações e frameworks utilizados? | Documento de processo + evidência de últimas correções aplicadas | Inspecionado | | | |

## Riscos de Segurança Transversais

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| SEG-44 | A organização já sofreu algum incidente de segurança (ransomware, vazamento, comprometimento de conta) nos últimos 24 meses? Como foi identificado e tratado? | Registro/relatório do incidente e do plano de resposta executado (ausência de incidente reportado não é tratada como evidência de segurança) | Inspecionado | | | |
| SEG-45 | Existe programa de conscientização em segurança da informação para os colaboradores (treinamento, simulação de phishing)? | Material de treinamento + relatório de simulação de phishing com taxa de clique | Inspecionado | | | |
| SEG-46 | Qual o percentual de colaboradores ativos que concluíu o treinamento obrigatório de conscientização em segurança no último ciclo? | Relatório de conclusão de treinamento com população total de colaboradores ativos, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-47 | Existe política formal de segurança da informação aprovada e comunicada à organização? | Documento de política assinado/aprovado e evidência de comunicação | Inspecionado | | | |
| SEG-48 | Qual o percentual de dispositivos móveis e notebooks corporativos com criptografia de disco habilitada (BitLocker/FileVault)? | Print de status de criptografia por dispositivo, via console de gestão, com população total de dispositivos, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-49 | Existe processo de classificação de dados sensíveis (ex.: dados de clientes, cargas, financeiros) que oriente controles de acesso e retenção? | Documento de classificação de dados | Inspecionado | | | |
| SEG-50 | Qual o percentual dos principais fornecedores/parceiros com acesso à rede ou sistemas da empresa que passaram por avaliação de risco de segurança? | Relatório de avaliação de risco de fornecedores com população total de fornecedores com acesso, amostra verificada e critério de seleção | Testado por amostragem | | | |
| SEG-51 | Existe monitoramento de segurança centralizado (SIEM ou equivalente) que correlacione eventos de diferentes fontes (rede, endpoint, identidade)? | Print de dashboard de monitoramento centralizado | Inspecionado | | | |
| SEG-52 | O monitoramento de segurança (SOC) é terceirizado ou interno? Qual o tempo médio de detecção (MTTD) e de resposta (MTTR) a incidentes/alertas nos últimos 12 meses? | Relatório de incidentes/alertas do período com população total, amostra verificada e critério de seleção, informando MTTD/MTTR calculados sobre a amostra | Testado por amostragem | | | |
| SEG-53 | Existe segregação clara de responsabilidades entre o SOC (detecção/monitoramento) e o time de TI interno (execução de remediação), documentada em contrato/SLA? | Contrato/SLA com matriz de responsabilidades SOC x TI interna | Inspecionado | | | |
| SEG-54 | Existe processo formal de gestão de exceções à política de segurança da informação (ex.: sistema legado sem suporte a controle exigido), com registro, aprovação, prazo de validade e revisão periódica? | Documento de processo de exceções + registro das exceções vigentes com data de aprovação e próxima revisão | Inspecionado | | | |
| SEG-55 | Existe plano de resposta a incidentes (IRP) formalizado e testado (exercício tabletop/simulação) nos últimos 12 meses? | Documento do IRP + relatório/ata do último exercício de simulação | Inspecionado | | | |

---

*Questionário a ser aplicado na entrevista com Fernanda Costa (Gerente de TI), conforme agenda de 22 a 26 de setembro de 2026. Toda pergunta com verificação ativa (cruzamento de listas, inspeção acompanhada, amostragem sobre população de itens) deve ser priorizada sobre autodeclaração verbal — nenhuma senha administrativa em texto aberto deve ser solicitada; inspeções devem ser acompanhadas pelo responsável técnico interno. Nenhuma resposta baseada apenas em declaração verbal do entrevistado, sem evidência anexada, pode sustentar uma classificação de controle "Adequado" no diagnóstico — e toda pergunta "Testado por amostragem" sem população, amostra e critério de seleção explícitos na resposta será classificada como "Não evidenciado", independentemente do percentual alegado.*
