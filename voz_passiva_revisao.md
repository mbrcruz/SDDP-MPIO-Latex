# Voz passiva na dissertação — checklist de revisão por seção

Levantamento automático das construções em **voz passiva** no texto, por capítulo e seção.
Duas categorias: **analítica** (*ser/estar* + particípio, ex.: "foi incorporada") e **sintética** (partícula apassivadora *se* + verbo transitivo, ex.: "adota-se").
Construções pronominais/impessoais que **não** são voz passiva (*torna-se, trata-se, concentra-se, espera-se, observa-se, mostra-se*) foram deixadas de fora de propósito.
**Totais:** 108 construções analíticas, 10 sintéticas.



## Cap. 1 — Introdução

### Contexto

- **L28** — passiva analítica: *foi estendido*  
  "processos em aplicações HPC, foi estendido a partir do MPI-2 com a"

### Motivação

- **L51** — passiva analítica: *é utilizado*  
  "(SDDP) é amplamente utilizado para o planejamento e"
- **L53** — passiva analítica: *é operado*  
  "Interligado Nacional (SIN) é operado pelo Operador Nacional do"
- **L59** — passiva analítica: *é avaliada*  
  "é avaliada em larga escala sobre um conjunto amplo de cenários ---"
- **L82** — passiva analítica: *são acentuados*  
  "Esses gargalos são acentuados pela expansão dos ambientes"

### Objetivos e Contribuições

- **L109** — passiva analítica: *é avaliado*  
  "Benders é avaliado em larga escala sobre múltiplos cenários para"

### Organização

- **L165** — passiva analítica: *são introduzidos*  
  "No Capítulo são introduzidos os principais"
- **L174** — passiva analítica: *é detalhada*  
  "Capítulo é detalhada a proposta de"
- **L181** — passiva analítica: *são discutidos*  
  "Capítulo são discutidos os"
- **L183** — passiva analítica: *são resumidos*  
  "Finalmente, no Capítulo são resumidos os"


## Cap. 2 — Fundamentação Teórica

### MPI, protocolos de comunicação e operações paralelas de arquivos

- **L162** — passiva analítica: *é adequado*  
  "é adequado quando cada processo produz blocos naturalmente"
- **L186** — passiva analítica: *é recomendado*  
  "Esse padrão é recomendado quando a aplicação possui fases bem definidas de"
- **L201** — passiva analítica: *é verificada*  
  "A conclusão é verificada posteriormente por chamadas como"

### Sistema de arquivos paralelo Lustre

- **L314** — passiva analítica: *são persistidos*  
  "metadados propriamente ditos são persistidos em um ou mais"
- **L322** — passiva analítica: *é realizado*  
  "O armazenamento dos dados é realizado pelos Object Storage Servers"
- **L343** — passiva analítica: *é dividido*  
  "striping, na qual um arquivo é dividido em blocos de tamanho fixo"
- **L348** — passiva analítica: *é espalhado*  
  "o stripe count, que indica em quantos OSTs o arquivo é espalhado."
- **L350** — passiva analítica: *sejam lidas*  
  "que diferentes partes sejam lidas ou escritas em paralelo, multiplicando a"
- **L357** — passiva analítica: *são alocados*  
  "Lustre. Com stripe count igual a 4, os blocos são alocados de"

### Ambientes computacionais

- **L372** — passiva analítica: *foram conduzidos*  
  "Os experimentos deste trabalho foram conduzidos em dois ambientes de"
- **L382** — passiva analítica: *foi desenvolvido*  
  "microssegundos. Já o InfiniBand foi desenvolvido especificamente para"

### Ambiente AWS

- **L414** — passiva analítica: *é exposta*  
  "topologia física dos nós não é exposta diretamente ao usuário. A AWS"
- **L420** — passiva analítica: *foram alocados*  
  "nós dos experimentos foram alocados em uma única zona. Para reduzir ainda"
- **L421** — passiva sintética: *utilizou-se*  
  "mais a latência de comunicação, utilizou-se um Placement Group do"
- **L425** — passiva analítica: *sendo recomendada*  
  "comunicação da nuvem ao de um cluster dedicado, sendo recomendada"
- **L428** — passiva analítica: *é provisionado*  
  "Lustre também é provisionado em uma única zona de disponibilidade,"

### Ambiente de supercomputação: Santos Dumont

- **L440** — passiva analítica: *são interligados*  
  "sua topologia é fixa e conhecida, e seus nós são interligados por uma rede"
- **L454** — passiva analítica: *foi explorado*; passiva sintética: *Utilizou-se*  
  "caminho não foi explorado nos experimentos deste trabalho. Utilizou-se a"

### Algoritmo SDDP

- **L483** — passiva analítica: *é indexado*  
  "determinísticos: cada subproblema é indexado por um par"
- **L493** — passiva analítica: *é avaliada*  
  "convergência, a política já fixa é avaliada em larga escala sobre um"
- **L506** — passiva analítica: *são particionados*  
  "sem sincronização durante a execução. Os cenários são particionados"

### Comparação dos formatos dos resultados

- **L552** — passiva analítica: *são organizados*  
  "Os resultados produzidos pelo SDDP são organizados em arquivos associados aos"
- **L556** — passiva analítica: *sejam registradas*  
  "interligações ou outros componentes cujas grandezas sejam registradas na saída"
- **L562** — passiva analítica: *são agregados*  
  "$(estágio, cenário)$ são agregados em poucos blocos"
- **L566** — passiva analítica: *é detalhado*  
  "lado, cada estágio é detalhado em horas individuais. Para um estágio mensal de"
- **L574** — passiva analítica: *é representada*  
  "é representada por um pequeno conjunto de blocos de carga; no formato horário,"
- **L575** — passiva analítica: *é representada*  
  "ela é representada por uma sequência de horas. A Figura"

### Arquitetura atual de E/S do SDDP

- **L651** — passiva analítica: *é designado*  
  "rank 1, denominado processo escritor) é designado para realizar"
- **L658** — passiva analítica: *são gravados*  
  "dados são gravados em um sistema de arquivos distribuído. A"
- **L674** — passiva analítica: *está relacionada*  
  "limitações de escalabilidade nessa arquitetura está relacionada ao"
- **L690** — passiva analítica: *será referido*  
  "Para efeitos desta dissertação, o rank 0 será referido como"


## Cap. 3 — Paralelização dos Mecanismos de E/S

### Modelo de execução

- **L65** — passiva analítica: *é representada*  
  "esse motivo, sua linha é representada integralmente como comunicação."

### Detalhes de implementação

- **L125** — passiva analítica: *são implementados*  
  "escrita dos arquivos de entrada e saída, são implementados como uma"
- **L131** — passiva analítica: *foi preservada*  
  "estrutura principal do algoritmo: a lógica de simulação foi preservada e as"

### Implementação das escritas independentes

- **L149** — passiva analítica: *são utilizadas*  
  "menores que 128 KB, são utilizadas operações assíncronas, permitindo que o"
- **L165** — passiva sintética: *Adota-se*  
  "Adota-se, portanto, um limite de 128 KB para separar os dois"
- **L220** — passiva sintética: *elimina-se*  
  "de resultado, elimina-se o risco de escritas concorrentes incidirem"
- **L225** — passiva analítica: *é calculado*  
  "escrita é calculado a partir da posição lógica do cenário no arquivo"
- **L251** — passiva analítica: *é dado*  
  "anteriormente. O positioning é dado por offset explícito:"
- **L252** — passiva analítica: *é derivada*  
  "a posição de destino é derivada da posição lógica do cenário no arquivo"
- **L254** — passiva analítica: *é escolhido*  
  "arquivo. O synchronism é escolhido por bloco: o caminho não"
- **L255** — passiva analítica: *é adotado*  
  "bloqueante (MPI_File_iwrite_at) é adotado para blocos menores que"
- **L258** — passiva analítica: *são serializados*  
  "valores dos elementos do sistema elétrico são serializados em um registro e"
- **L260** — passiva analítica: *são acumulados*  
  "$(estágio, cenário)$ são acumulados em memória, emitindo-se"
- **L270** — passiva analítica: *é atingido*  
  "escrita e, em regime, raramente é atingido. Ao final, as escritas ainda"

### Formato dos resultados

- **L316** — passiva analítica: *foi adotada*  
  "utilizado pelo SDDP. Essa decisão foi adotada para manter a compatibilidade"
- **L319** — passiva analítica: *são gravados*  
  "concentra-se na forma como os dados são gravados, sem alterar a estrutura"
- **L326** — passiva analítica: *é identificado*  
  "lógica dos arquivos binários de resultado. Cada registro é identificado"
- **L328** — passiva analítica: *são armazenados*  
  "hora. A partir da quarta coluna são armazenados os valores associados aos"
- **L334** — passiva analítica: *seja registrada*  
  "sistema elétrico cuja grandeza seja registrada na saída da simulação. Os"
- **L367** — passiva analítica: *é alocado*  
  "No Lustre, cada bloco gravado nos arquivos de resultado é alocado em um"

### Instrumentação

- **L404** — passiva analítica: *foram instrumentadas*  
  "implementação proposta foram instrumentadas no módulo de persistência"
- **L406** — passiva analítica: *foi incorporada*  
  "MPI-IO foi incorporada nesta proposta. Os cronômetros foram"
- **L409** — passiva analítica: *é adequada*  
  "resolução é adequada para temporização de operações de E/S e"
- **L415** — passiva analítica: *foi mantida*  
  "A instrumentação foi mantida coerente entre as duas implementações, de"

### Registros gerados pela instrumentação

- **L427** — passiva analítica: *são persistidos*  
  "Os tempos coletados são persistidos em arquivos de log textuais"
- **L466** — passiva analítica: *são derivadas*  
  "A partir desses arquivos, as métricas são derivadas por agregação. As"

### Tempo de computação

- **L477** — passiva analítica: *é obtido*  
  "intervalo é obtido a partir do temporizador Hourly simulation"

### Tempo de MPI_File_open/MPI_File_close

- **L496** — passiva analítica: *Estão incluídas*  
  "pontos de coordenação entre processos. Estão incluídas, nessa categoria,"

### Banda agregada média percebida pela aplicação

- **L564** — passiva sintética: *Define-se*  
  "Define-se, neste trabalho, como banda agregada percebida pela"
- **L567** — passiva analítica: *É calculada*  
  "aproveitar sob seu modelo de execução. É calculada a partir dos registros do mpiio-p.log"
- **L569** — passiva sintética: *computa-se*  
  "fixa $$. Para cada janela $w$, computa-se a razão entre o volume"
- **L591** — passiva analítica: *é calculada*  
  "A banda percebida é calculada em função do tempo de bloqueio das"


## Cap. 4 — Avaliações

### (início do capítulo)

- **L15** — passiva analítica: *foram considerados*  
  "principal deste estudo, foram considerados 1.536 cenários em ambos os"
- **L18** — passiva analítica: *foram executadas*  
  "Para cada configuração avaliada, foram executadas cinco repetições; os"
- **L37** — passiva analítica: *sendo esperado*  
  "trabalho por nó, sendo esperado, idealmente, que o tempo total de execução"
- **L47** — passiva analítica: *foi considerado*  
  "O tamanho dos blocos de dados foi considerado um fator determinante para a"
- **L51** — passiva analítica: *é dominada*  
  "Observa-se que a distribuição é dominada por blocos de dados pequenos:"
- **L58** — passiva analítica: *será avaliado*  
  "Adicionalmente, será avaliado o tempo de envio dos blocos de dados"
- **L71** — passiva analítica: *está associada*  
  "está diretamente associada à organização dos arquivos de resultado"
- **L72** — passiva analítica: *foram gerados*  
  "produzidos pelo SDDP. Nos experimentos foram gerados 117 arquivos"
- **L75** — passiva analítica: *são acumulados*  
  "$(estágio, cenário)$ são acumulados em memória e"
- **L78** — passiva analítica: *é gravado*  
  "dia do mês é gravado individualmente, sem agregação entre dias."

### Experimento AWS

- **L88** — passiva analítica: *foi configurado*  
  "O Experimento AWS foi configurado na nuvem da Amazon Web Services (AWS),"
- **L103** — passiva sintética: *utilizou-se*  
  "utilizou-se a biblioteca MPICH2 versão 3.2 e um sistema de arquivos"
- **L105** — passiva analítica: *foi configurado*  
  "1,165 TB. O stripe count foi configurado como 10, com"
- **L108** — passiva sintética: *configurou-se*  
  "capítulo, configurou-se um rank por núcleo físico, totalizando"

### Avaliação da implementação atual

- **L144** — passiva sintética: *Soma-se*  
  "Soma-se a esse efeito a heterogeneidade entre envios locais e remotos."
- **L151** — passiva analítica: *é acentuado*  
  "nó escritor. Esse efeito é particularmente acentuado na configuração"
- **L163** — passiva analítica: *são apresentados*  
  "I/O e comunicação são apresentados separadamente."
- **L169** — passiva analítica: *é calculada*  
  "eficiência e percentual de I/O. A eficiência é calculada em relação à"
- **L604** — passiva analítica: *é calculada*  
  "E/S e comunicação. A eficiência é calculada em relação à base de 2 nós."

### Avaliação da implementação MPI-IO com escritas independentes

- **L210** — passiva analítica: *são apresentados*  
  "I/O, comunicação e MPI_File_open/MPI_File_close são apresentados separadamente."
- **L657** — passiva analítica: *é calculada*  
  "E/S, comunicação e MPI_File_open/MPI_File_close. A eficiência é calculada em relação"

### Análise comparativa

- **L247** — passiva analítica: *são consolidados*  
  "Os resultados das duas subseções anteriores são consolidados visualmente"
- **L267** — passiva analítica: *são calculadas*  
  "Experimento AWS. A melhoria no total e a melhoria de I/O são calculadas"
- **L324** — passiva analítica: *sejam enviados*  
  "processos MPI, permitindo que múltiplos fluxos de dados sejam enviados"
- **L353** — passiva analítica: *é dominado*  
  "que, em pequena escala, o tempo de execução é dominado pela computação e"
- **L388** — passiva analítica: *são executadas*  
  "MPI_File_open/MPI_File_close são executadas"
- **L688** — passiva analítica: *são consolidados*  
  "Os resultados das duas subseções anteriores são consolidados visualmente"
- **L749** — passiva analítica: *é amortizado*  
  "escala, em que o custo fixo da camada MPI-IO ainda não é amortizado"
- **L901** — passiva analítica: *é reduzido*  
  "implementação atual; o tempo de E/S é reduzido em 87,3%"

### Avaliação do impacto do número de OSTs

- **L451** — passiva analítica: *está relacionada*  
  "está diretamente relacionada ao grau de paralelismo de E/S disponível,"
- **L458** — passiva analítica: *foi obtida*  
  "Tabela ); a configuração de 4 OSTs foi obtida em"
- **L466** — passiva analítica: *foram realizados*  
  "Para esta avaliação, foram realizados experimentos com a abordagem"
- **L497** — passiva analítica: *seja realizada*  
  "cálculo cresce. Embora a escrita seja realizada em paralelo por meio de"

### Experimento SDumont

- **L549** — passiva analítica: *foram utilizados*  
  "foram utilizados até 32 nós de processamento, cada um equipado com dois"
- **L555** — passiva analítica: *foi utilizada*  
  "aplicações paralelas de larga escala. Nos experimentos, foi utilizada a"
- **L558** — passiva analítica: *é composta*  
  "implementação do Lustre é composta por 1 nó MDS (com 1 MDT) e 6 nós OSSs"
- **L559** — passiva analítica: *foi configurado*  
  "(cada um servindo 1 OST). O stripe count foi configurado como 6,"
- **L567** — passiva analítica: *é compartilhado*  
  "sistema de arquivos do SDumont é compartilhado com outras cargas de"


## Cap. 5 — Trabalhos Relacionados

### (início do capítulo)

- **L20** — passiva analítica: *foi adotada*  
  "escrita ao filesystem. Essa abordagem não foi adotada nesta"


## Cap. 6 — Conclusões e Trabalhos Futuros

### (início do capítulo)

- **L48** — passiva analítica: *são agregados*  
  "$(estágio, cenário)$ são agregados em uma única"
- **L49** — passiva analítica: *foram agrupados*  
  "escrita ---, os dias não foram agrupados nos arquivos diários. O"
- **L50** — passiva analítica: *é mitigado*  
  "impacto desse padrão fragmentado é parcialmente mitigado pela"

### Trabalhos futuros

- **L66** — passiva sintética: *identificam-se*  
  "A partir dos resultados e limitações apresentados, identificam-se"
- **L73** — passiva analítica: *é feito*  
  "analogamente ao que já é feito nos arquivos horários ---,"
