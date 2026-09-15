---
layout: ../../../layouts/ClientDoc.astro
title: "Questionário — Infraestrutura e Redes"
cliente: "Super Logística"
voltarHref: "/assessment/super-logistica/"
---

# Questionário — Infraestrutura e Redes
Cliente: Super Logística | Módulo: Infraestrutura e Redes
Interlocutor: Bruno Alves, Coordenador de Infraestrutura

> Padrão de verificação: toda pergunta declara um Método de Verificação
> Exigido (Declarado / Inspecionado / Testado por amostragem). Perguntas
> "Testado por amostragem" exigem, na resposta, o tamanho da população, o
> tamanho da amostra efetivamente verificada e o critério de seleção da
> amostra — ver Regra de Amostragem em `maturity-scales.md` Seção 5.3.
> Percentual sem essas três informações é tratado como evidência
> insuficiente ("Não evidenciado") no diagnóstico, independentemente do que
> for alegado em entrevista.

## Rede e Conectividade

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-01 | Quantos sites/datacenters (próprios ou de terceiros) compõem o escopo de infraestrutura deste assessment, e qual a função de cada um (produção, contingência, filial, CD)? | Relação de sites com função de cada um | Declarado | | | |
| INF-02 | Existe diagrama de topologia de rede atualizado (últimos 12 meses), cobrindo todos os sites/datacenters em escopo? | Diagrama de rede com data de última revisão | Inspecionado | | | |
| INF-03 | Os links de internet (e entre unidades/filiais, se houver) possuem redundância com teste de failover formal, documentado com data e resultado? | Registro/log do último teste de failover, contendo data do teste e resultado (sucesso/falha/tempo de chaveamento) — declaração verbal sem esse registro não é aceita como evidência | Inspecionado | | | |
| INF-04 | Quais protocolos e serviços de borda (VPN, DNS, DHCP) estão em uso e quem é o responsável formal por sua administração? | Documentação de arquitetura de borda + matriz de responsáveis | Inspecionado | | | |
| INF-05 | Qual o percentual de switches, roteadores e firewalls com firmware/SO de rede em versão suportada pelo fabricante (sem EOL/EOS)? | (1) Tamanho da população total de equipamentos de rede em escopo; (2) tamanho da amostra efetivamente inspecionada, aplicando a Regra de Amostragem — ≤25 itens testa 100%, 26-100 amostra mínima 25, 101-500 amostra mínima 40 ou 10% (o maior), >500 amostra mínima 60 ou 8% (o maior); (3) critério de seleção da amostra (aleatória, todos os críticos, por site); (4) evidência de versão de firmware/SO e status EOL/EOS por item amostrado, confrontado com a data oficial do fabricante | Testado por amostragem | | | |
| INF-06 | Existe inventário formal de fim de vida/fim de suporte (EOL/EOS) dos equipamentos de rede (switches, roteadores, firewalls), com a data específica publicada pelo fabricante para cada modelo em uso? | Planilha/relatório de inventário listando modelo, versão, data de EOL e data de EOS por fabricante (não apenas "está desatualizado" — datas específicas) | Inspecionado | | | |
| INF-07 | Existe backup das configurações de switches, roteadores e firewalls, com teste de restauração já realizado e documentado? | Rotina de backup de configuração + evidência de teste de restauração (data e resultado) | Inspecionado | | | |
| INF-08 | Há monitoramento ativo de disponibilidade e latência dos links de rede, com alertas configurados e histórico consultável? | Print/relatório do console de monitoramento de rede, com histórico de pelo menos 90 dias | Inspecionado | | | |
| INF-09 | Qual a capacidade real medida (utilização média e de pico) dos links de internet nos últimos 90 dias, comparada à capacidade nominal contratada junto ao provedor? | Relatório de utilização de banda (medição real) confrontado com o contrato/SLA do provedor que declara a capacidade nominal — não aceitar apenas a capacidade nominal contratada como proxy de capacidade real disponível | Inspecionado | | | |

## Segmentação e VLANs

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-10 | A rede é segmentada em zonas distintas (administração, servidores, operação logística, visitantes/Wi-Fi público)? | Diagrama de VLANs ou configuração de switches/firewall | Inspecionado | | | |
| INF-11 | Existe controle de tráfego (ACL/firewall) entre as VLANs segmentadas, ou a segmentação é apenas lógica sem restrição de fluxo? | Regras de ACL/firewall entre VLANs, exportadas do equipamento | Inspecionado | | | |
| INF-12 | Redes de operação (ex.: coletores, TMS/WMS, equipamentos de armazém) estão isoladas da rede corporativa administrativa? | Diagrama de segmentação operação vs. administração + regras de isolamento | Inspecionado | | | |
| INF-13 | O acesso Wi-Fi de visitantes está isolado da rede interna de produção? | Configuração de VLAN/SSID de convidados isolada, com teste de tentativa de acesso cruzado | Inspecionado | | | |
| INF-14 | Existe revisão periódica documentada das regras de segmentação para identificar exceções acumuladas (regras obsoletas, liberações temporárias nunca revogadas)? | Registro/ata de revisão periódica de regras de firewall/ACL, com data da última revisão | Inspecionado | | | |
| INF-15 | A separação entre zonas de criticidade distinta (ex.: servidores de produção vs. administração) é física (racks/gabinetes distintos, cabeamento dedicado) ou apenas lógica (mesma infraestrutura física, segmentação só por VLAN)? Em caso de comprometimento do switch/rack físico, quais zonas lógicas seriam afetadas simultaneamente? | Planta física do datacenter/rack + mapeamento de quais VLANs compartilham o mesmo equipamento físico/rack | Inspecionado | | | |

## Servidores Físicos

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-16 | Existe inventário de servidores físicos com função, dependências e criticidade documentadas para cada item? | Planilha/CMDB de servidores físicos | Inspecionado | | | |
| INF-17 | Qual o percentual de servidores físicos críticos com componentes redundantes (fontes de alimentação, discos em RAID, placas de rede) efetivamente confirmado por inspeção técnica? | (1) Tamanho da população total de servidores físicos; (2) tamanho da amostra inspecionada conforme a Regra de Amostragem (Seção 5.3); (3) critério de seleção; (4) especificação técnica confirmando redundância por item amostrado (não apenas a ficha técnica de compra, mas o estado atual do equipamento) | Testado por amostragem | | | |
| INF-18 | Qual o percentual de servidores físicos em produção cobertos por contrato de suporte/garantia vigente com o fabricante ou revenda? | (1) Tamanho da população total de servidores físicos; (2) tamanho da amostra verificada (Seção 5.3); (3) critério de seleção; (4) contrato de suporte com data de vencimento por item amostrado | Testado por amostragem | | | |
| INF-19 | O ambiente físico (sala de servidores/rack) possui controle de energia (nobreak/gerador) e climatização adequada, com manutenção preventiva registrada? | Especificação de nobreak/gerador + registro de manutenção preventiva com datas | Inspecionado | | | |
| INF-20 | Existe processo de atualização de firmware dos servidores físicos, com janela de mudança formalizada e aprovação prévia? | Registro de janela de mudança (change) para a última atualização de firmware realizada | Inspecionado | | | |
| INF-21 | Existe inventário formal de fim de vida/fim de suporte (EOL/EOS) dos servidores físicos, com a data específica publicada pelo fabricante para cada modelo em uso? | Planilha/relatório listando modelo, data de EOL e data de EOS por fabricante para cada servidor físico | Inspecionado | | | |

## Virtualização e Clusters

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-22 | O ambiente de virtualização possui cluster de hosts com failover automático (HA) configurado E testado, com data e resultado do teste documentados? | Configuração de cluster/HA do hypervisor + registro de teste de failover contendo data, cenário testado (ex.: queda simulada de host) e resultado | Inspecionado | | | |
| INF-23 | Existe inventário de máquinas virtuais com função, criticidade e dependências documentadas? | Planilha/CMDB de VMs | Inspecionado | | | |
| INF-24 | Qual a capacidade real medida de utilização do cluster (CPU/memória, uso médio e de pico dos últimos 90 dias) comparada à capacidade nominal instalada, e o cluster suportaria a perda de ao menos um host (N+1) sem degradação crítica nesse cenário real de uso? | Relatório de utilização real do cluster (não a capacidade nominal declarada em ficha técnica) + simulação/cálculo de capacidade remanescente em cenário de perda de 1 host | Inspecionado | | | |
| INF-25 | Qual o percentual de hosts do cluster de virtualização em versão de hypervisor suportada pelo fabricante, com patches de segurança aplicados dentro do prazo definido internamente? | (1) Tamanho da população total de hosts; (2) tamanho da amostra verificada (Seção 5.3, população provavelmente ≤25 → testar 100%); (3) critério de seleção; (4) relatório de versão e histórico de patches por host amostrado | Testado por amostragem | | | |
| INF-26 | Existe processo de backup de configuração do ambiente de virtualização (cluster, vSwitches, políticas de HA/DRS), com teste de restauração já realizado? | Rotina de backup de configuração do hypervisor + evidência de teste de restauração | Inspecionado | | | |

## Storage

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-27 | Existe inventário do(s) storage(s) em uso, com capacidade total, capacidade utilizada e projeção de esgotamento? | Relatório de inventário e utilização de storage, com data de extração | Inspecionado | | | |
| INF-28 | O storage possui redundância de componentes (controladoras, fontes, discos em RAID/proteção equivalente) com teste de failover de controladora documentado (data e resultado)? | Especificação técnica + registro de teste de failover de controladora contendo data e resultado | Inspecionado | | | |
| INF-29 | Há monitoramento de saúde dos discos/volumes com alertas configurados para falhas iminentes (ex.: SMART, previsão de falha de disco)? | Print/relatório do console de monitoramento de storage, com histórico de alertas | Inspecionado | | | |
| INF-30 | Existe segregação de dados críticos (ex.: bases de TMS/WMS) em volumes com política de proteção reforçada (RAID mais robusto, snapshot mais frequente, tier de disco dedicado)? | Mapeamento de volumes por criticidade de dado, com a política de proteção aplicada a cada um | Inspecionado | | | |
| INF-31 | Qual a capacidade real medida de performance (IOPS, throughput, latência) do storage nos últimos 90 dias, comparada à capacidade nominal declarada pelo fabricante/integrador na aquisição? | Relatório de performance real do storage (medição de IOPS/throughput/latência) confrontado com a especificação nominal do equipamento | Inspecionado | | | |

## Redundância e Disponibilidade

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-32 | De uma população total de componentes críticos de infraestrutura (rede, servidores, storage, virtualização) mapeados, quantos NÃO possuem redundância hoje e isso está documentado como risco conhecido (matriz de SPOF)? | (1) Tamanho da população total de componentes críticos mapeados; (2) tamanho da amostra/cobertura verificada (Seção 5.3); (3) critério de seleção; (4) matriz/registro de pontos únicos de falha (SPOF) com os itens sem redundância listados | Testado por amostragem | | | |
| INF-33 | Dos itens declarados como "redundantes" na infraestrutura, qual percentual possui evidência de teste de failover realizado e documentado (com data e resultado) nos últimos 12 meses? | (1) Tamanho da população total de itens declarados redundantes; (2) tamanho da amostra de registros de teste verificados (Seção 5.3); (3) critério de seleção; (4) registro de teste de failover por item amostrado, com data e resultado | Testado por amostragem | | | |
| INF-34 | Existe SLA interno ou contratual de disponibilidade definido para os serviços de infraestrutura crítica, com metas numéricas (ex.: 99,9%)? | Documento de SLA/acordo de nível de serviço, com metas e período de vigência | Inspecionado | | | |
| INF-35 | Já houve incidente de indisponibilidade nos últimos 12 meses causado por ausência de redundância? Qual foi a causa raiz documentada e como foi tratado? | Registro/ticket do incidente, com causa raiz documentada e tempo de indisponibilidade (MTTR) | Inspecionado | | | |

## Monitoramento de Capacidade

| Ref | Pergunta | Evidência Esperada | Método de Verificação Exigido | Resposta do Entrevistado | Evidência Anexada (Sim/Não/Parcial + referência) | Complemento do Entrevistador |
|---|---|---|---|---|---|---|
| INF-36 | Existe ferramenta de monitoramento de capacidade (CPU, memória, storage, rede) com histórico e alertas configurados? | Print/relatório do console de monitoramento de capacidade, com histórico de pelo menos 90 dias | Inspecionado | | | |
| INF-37 | Há análise de tendência de crescimento (histórico de uso) usada para prever necessidade de expansão de infraestrutura? | Relatório de tendência de capacidade/crescimento histórico, com projeção documentada | Inspecionado | | | |
| INF-38 | Os alertas de capacidade (limiares de uso) são revisados periodicamente e direcionados a um responsável formalmente definido? | Matriz de responsáveis por alertas + registro de revisão periódica dos limiares, com data da última revisão | Inspecionado | | | |
| INF-39 | Existe plano de expansão de capacidade formalizado para os próximos 6-12 meses, considerando o crescimento projetado da operação logística? | Plano de capacidade/expansão documentado, com prazos e investimentos previstos | Inspecionado | | | |
| INF-40 | Consolidando servidores, storage e rede, qual a capacidade real medida (uso médio e de pico dos últimos 90 dias) de cada camada, comparada à capacidade nominal instalada? Em quanto tempo, na tendência atual, cada camada atinge seu limite de capacidade nominal? | Relatório consolidado de capacidade real por camada (servidores/storage/rede), confrontado com a capacidade nominal instalada, com estimativa de tempo até saturação por camada | Inspecionado | | | |
