---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Endpoint Management"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Sistemas Operacionais e Endpoints
Cliente: Super Logística | Módulo: Endpoint Management

> Padrão de rigor de working paper (maturity-scales.md Seção 5). Toda
> pergunta que envolve percentual, cobertura de frota ou afirmação sobre uma
> população de endpoints é "Testado por amostragem": a resposta só é válida
> se declarar (1) população total, (2) amostra efetivamente verificada e (3)
> critério de seleção da amostra, conforme a Regra de Amostragem — ≤25 itens
> → 100%; 26-100 → mín. 25; 101-500 → mín. 40 ou 10%; >500 → mín. 60 ou 8%.
> Percentual sem essas três informações é evidência insuficiente e será
> classificado "Não evidenciado" na Fase 4, independentemente do valor
> declarado.

## Versão de SO e Patch Management

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-01 | Qual o percentual da frota (desktops + notebooks) rodando sistema operacional fora de suporte do fabricante (EOL/EOS)? | Relatório de inventário de SO por versão, extraído de ferramenta de gestão de parque. Amostragem obrigatória: informar população total de endpoints, amostra efetivamente verificada e critério de seleção (aleatória, todos os críticos, ou por unidade/site), conforme Regra de Amostragem. | Testado por amostragem | | | |
| EPT-02 | Qual o percentual da frota com todos os patches críticos de segurança instalados dentro do SLA formalmente definido? | Relatório de compliance de patch (ex.: WSUS, SCCM, Intune ou equivalente). Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-03 | Existe política formal de atualização/patch com periodicidade definida (janela de aplicação, prazo máximo de defasagem)? | Documento de política de patch management | Inspecionado | | | |
| EPT-04 | Qual o SLA formalmente definido (em número de dias corridos) entre a disponibilização de um patch crítico pelo fabricante e sua aplicação obrigatória em toda a frota? | Documento de política/SLA de patch com prazo numérico explícito | Inspecionado | | | |
| EPT-05 | Nos últimos 3 meses, qual foi o tempo médio real decorrido entre a disponibilização de cada patch crítico e sua aplicação efetiva na frota, e qual percentual dos patches críticos publicados nesse período foi aplicado dentro do SLA definido (EPT-04)? Não basta confirmar que existe processo — é necessário o dado real medido. | Relatório de tempo de aplicação de patch por evento crítico (ex.: relatório de compliance histórico da ferramenta de patch, com datas de publicação e de aplicação). Amostragem obrigatória: população total de patches críticos publicados no período (ou de endpoints, se medido por dispositivo), amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-06 | Qual o processo de aplicação de patches: manual por técnico, script agendado ou ferramenta central automatizada? | Demonstração da ferramenta/processo de distribuição de patches | Inspecionado | | | |
| EPT-07 | Há inventário atualizado com a versão exata de SO (build/edição) de 100% dos endpoints, incluindo os remotos e os que raramente se conectam à rede corporativa? | Extrato completo do inventário de ativos de endpoint, com data da última atualização de cada registro. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-08 | Notebooks de uso em campo/operação (ex.: motoristas, técnicos externos, força de vendas) atingem o mesmo SLA de patch definido em EPT-04, ou o processo é diferente/mais lento por não se conectarem regularmente à rede corporativa? Informar o percentual de conformidade de cada grupo separadamente. | Relatório de compliance de patch segmentado por perfil de dispositivo (campo/operação vs. administrativo). Amostragem obrigatória: população total de cada grupo, amostra verificada em cada um e critério de seleção. | Testado por amostragem | | | |

## Padronização de Imagem

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-09 | Qual o percentual da frota provisionada a partir de uma imagem padrão corporativa (golden image)? | Documento de imagem padrão + relatório de conformidade de configuração. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-10 | Quantas versões/edições distintas de sistema operacional coexistem hoje no parque (ex.: Windows 10 Pro, Windows 11 Home, versões distintas de Linux)? | Relatório de inventário segmentado por versão/edição de SO, cobrindo 100% do parque registrado | Inspecionado | | | |
| EPT-11 | Existe processo formal e documentado de provisionamento de novo endpoint (do desempacotamento à entrega ao usuário)? | Procedimento documentado de provisionamento | Inspecionado | | | |
| EPT-12 | Softwares de terceiros essenciais (navegador, leitor de PDF, suíte de escritório, agente de segurança) são padronizados e distribuídos via imagem/ferramenta central, ou instalados manualmente por máquina? Qual o percentual de conformidade da frota com a lista padrão? | Lista de softwares padrão + relatório de conformidade de instalação. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-13 | Existe uma imagem/pacote de software padrão específico para notebooks de campo/operação, distinto do padrão administrativo (ex.: sem determinadas ferramentas administrativas, com aplicativos de operação específicos)? Qual o percentual de conformidade de cada grupo com sua respectiva imagem padrão? | Documento de imagem padrão segmentado por perfil + relatório de conformidade por grupo. Amostragem obrigatória: população total de cada grupo, amostra verificada e critério de seleção. | Testado por amostragem | | | |

## Configuração de Segurança e Privilégios Locais

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-14 | Qual o percentual de usuários comuns que possuem privilégio administrativo local na própria máquina? | Relatório de membros do grupo de administradores locais, extraído via GPO/ferramenta de gestão. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-15 | Existe política técnica (GPO ou equivalente) que impede a instalação de software não autorizado por usuários sem privilégio administrativo? | Configuração de GPO/política de restrição de software demonstrada | Inspecionado | | | |
| EPT-16 | Qual o percentual de endpoints com firewall local ativo e configurado conforme baseline corporativo? | Relatório de status de firewall local por dispositivo. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-17 | Qual o percentual de endpoints com agente de proteção (EDR/antivírus) ativo, atualizado e reportando ao console central? | Relatório de status de agente de segurança por dispositivo (console de gestão). Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-18 | A política de complexidade e expiração de senha local é aplicada tecnicamente (via GPO/diretório) ou depende apenas de orientação escrita? | Configuração de política de senha aplicada via GPO/diretório | Inspecionado | | | |
| EPT-19 | O nível de privilégio local concedido a usuários de notebooks de campo/operação é o mesmo aplicado aos usuários de dispositivos administrativos, ou existe perfil de restrição diferenciado (ex.: mais restritivo para campo, dado o maior risco de perda/furto)? Informar o percentual de conformidade de cada grupo com o baseline de privilégio mínimo. | Relatório de grupos locais de administração segmentado por perfil de dispositivo. Amostragem obrigatória: população total de cada grupo, amostra verificada e critério de seleção. | Testado por amostragem | | | |

## Criptografia e Bloqueio Automático

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-20 | Qual o percentual de notebooks/dispositivos móveis com criptografia de disco ativa (BitLocker ou equivalente)? | Relatório de status de criptografia por dispositivo, extraído do console central. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-21 | As chaves de recuperação de criptografia são armazenadas de forma centralizada e segura (ex.: Active Directory, Intune, cofre corporativo)? | Demonstração do repositório de chaves de recuperação | Inspecionado | | | |
| EPT-22 | Qual o percentual de endpoints com bloqueio automático de tela configurado com tempo de inatividade dentro do padrão de segurança definido? | Configuração de GPO de bloqueio automático + relatório de conformidade. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-23 | Desktops fixos também possuem criptografia de disco habilitada, ou a criptografia é restrita apenas a notebooks? Qual o percentual de desktops fixos com criptografia ativa? | Relatório de status de criptografia segmentado por tipo de dispositivo. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-24 | Notebooks de campo/operação — por estarem mais expostos a perda, furto ou extravio fora das instalações da empresa — possuem o mesmo percentual de criptografia ativa que os notebooks administrativos, ou há uma lacuna entre os dois grupos? | Relatório de status de criptografia segmentado por perfil de dispositivo (campo/operação vs. administrativo). Amostragem obrigatória: população total de cada grupo, amostra verificada e critério de seleção. | Testado por amostragem | | | |

## Controle de Dispositivos Externos

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-25 | Qual o percentual da frota com bloqueio ou controle técnico de portas USB/dispositivos externos de armazenamento? | Configuração de GPO/DLP de controle de dispositivos + relatório de aplicação. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-26 | Existe processo de autorização formal para liberação excepcional de uso de dispositivo externo (ex.: pendrive) em máquina específica? | Procedimento documentado de exceção + registro de aprovações | Inspecionado | | | |
| EPT-27 | Há registro/log de eventos de conexão de dispositivos externos nos endpoints, com retenção definida? | Configuração de log de eventos de dispositivo externo (SIEM ou agente local) demonstrada, com política de retenção documentada | Inspecionado | | | |
| EPT-28 | Qual o percentual de endpoints com controle técnico que impede a gravação de dados sensíveis em mídia removível não autorizada? | Configuração de política de DLP/controle de mídia removível + relatório de aplicação. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |

## BYOD e Dispositivos Não Corporativos

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-29 | A empresa permite o uso de dispositivos pessoais (BYOD) para acesso a recursos corporativos (e-mail, VPN, aplicações, arquivos)? | Confirmação verbal do modelo adotado (permitido, proibido, ou permitido apenas para perfis específicos) | Declarado | | | |
| EPT-30 | Existe política formal de BYOD definindo requisitos mínimos de segurança para o dispositivo pessoal ser autorizado a acessar recursos corporativos? | Documento de política de BYOD | Inspecionado | | | |
| EPT-31 | Quantos dispositivos BYOD estão atualmente registrados/autorizados a acessar recursos corporativos? | Relatório de dispositivos registrados no console de gestão (MDM/MAM) ou, na ausência de ferramenta, contagem declarada pelo responsável | Declarado | | | |
| EPT-32 | Qual o percentual de dispositivos BYOD autorizados que possuem controle técnico mínimo aplicado (MDM/MAM, criptografia, tela de bloqueio com senha, capacidade de wipe remoto seletivo)? | Relatório de conformidade de dispositivos BYOD extraído da ferramenta de MDM/MAM. Amostragem obrigatória: população total de dispositivos BYOD registrados, amostra verificada e critério de seleção — se a população for ≤25, testar 100%. | Testado por amostragem | | | |
| EPT-33 | Existe segregação técnica entre dados corporativos e pessoais em dispositivos BYOD (ex.: containerização, perfil de trabalho separado, acesso via VPN/aplicação restrita sem sincronização local), ou o acesso é irrestrito ao dispositivo pessoal inteiro? | Demonstração da configuração de segregação (perfil de trabalho, container, ou política de acesso restrito) | Inspecionado | | | |

## Ciclo de Vida de Dispositivos

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| EPT-34 | Existe processo formal de descarte seguro de dados (wipe/destruição) em equipamentos substituídos ou desativados? | Procedimento documentado de descarte seguro + registros de execução | Inspecionado | | | |
| EPT-35 | Qual o percentual da frota atual com idade superior ao ciclo de renovação/substituição definido pela política interna (ou, na ausência de política, superior a 4 anos)? | Relatório de inventário com data de aquisição por dispositivo. Amostragem obrigatória: população total, amostra verificada e critério de seleção. | Testado por amostragem | | | |
| EPT-36 | Existe política formal de ciclo de vida definindo prazos de aquisição, substituição e descarte por tipo de dispositivo? | Documento de política de ciclo de vida de ativos de endpoint | Inspecionado | | | |
| EPT-37 | Como é conduzido o processo de baixa patrimonial e atualização de inventário quando um equipamento é substituído ou descartado? | Procedimento de baixa patrimonial + registro de movimentação no inventário/CMDB | Inspecionado | | | |
| EPT-38 | O ciclo de renovação/substituição definido para notebooks de campo/operação (sujeitos a maior desgaste físico, transporte e uso externo intenso) é diferenciado do aplicado a notebooks administrativos? Qual o percentual de cada grupo dentro do prazo de renovação definido para o respectivo perfil? | Relatório de inventário com data de aquisição, segmentado por perfil de dispositivo (campo/operação vs. administrativo), e política de ciclo de vida (se diferenciada por perfil). Amostragem obrigatória: população total de cada grupo, amostra verificada e critério de seleção. | Testado por amostragem | | | |
