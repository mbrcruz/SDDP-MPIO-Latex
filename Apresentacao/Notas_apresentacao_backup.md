# Notas do apresentador — backup antes de apagar

Arquivo: Apresentacao_MPIO.pptx  ·  28 slides

## Slide 1 — Escalando a E/S do SDDP em Ambientes HPC: da Escrita Serializada as Escritas Paralelas com MPI-IO sobre Lustre

Capa. Preencher orientador e banca — ainda estão como placeholder no dissertacao.tex (pendência já mapeada na avaliação de banca).

## Slide 2 — Investigando Problemas de Escalabilidade de E/S no Algoritmo SDDP em Ambientes HPC

Capa. Preencher orientador e banca — ainda estão como placeholder no dissertacao.tex (pendência já mapeada na avaliação de banca).

## Slide 3 — O supercomputador mais rápido do mundo

GANCHO DE ABERTURA — deixar na tela enquanto a banca se acomoda. Não responder agora.

A foto estabelece MAGNITUDE, não a resposta: a plateia sente a escala da máquina antes da pergunta, sem que nada seja antecipado. Os números de apoio estão na linha sob o título.

A pergunta é sobre ESCALABILIDADE, não sobre quantos cores. A montagem entrega abundância dos dois lados — máquina enorme e tarefas de sobra — e deixa a pergunta em aberto. A resposta contraintuitiva (não, não com a arquitetura atual) é a tese, e volta no último slide.

Parâmetros condicionados como HIPOTÉTICO: você não rodou esse caso e o SHOTGUN não foi testado.

SHOTGUN: todos os problemas (estágio, cenário) resolvidos de forma independente, sem sincronização entre estágios — é o que libera o paralelismo máximo: 10.000 x 120 = 1.200.000 tarefas.

Escala contra o experimento (1.536 cenários x 3 estágios = 4.608 tarefas):
  - 260x mais tarefas
  - 864 milhões de registros horários contra 3,3 milhões = 260x mais dados a gravar
  - 1.200.000 ranks úteis = 8,7% dos cores do LineShine

CREDITAR A FOTO: acrescente a fonte da imagem (uma linha discreta no canto, ou menção verbal). É foto de terceiros e a defesa é sessão pública — creditar resolve.

NÃO prometer tempo de execução — não foi medido.

## Slide 4 — Introdução e Motivação

ENQUADRAMENTO: contexto de HPC, não de planejamento energético. A banca do PESC é de computação — o terreno seguro é o gargalo de E/S, não o modelo de operação.

Sequência de fala:
1) O SDDP entra APENAS como carga de trabalho. Simulação final = política já convergida, avaliada sobre muitos cenários; os cenários são independentes por construção, sem estado compartilhado nem coordenação — logo, bag-of-tasks (Cirne, 2003). Em resolução horária cada par (estágio, cenário) vira um bloco contíguo uma ordem de grandeza maior. Frase-chave: a tarefa não termina quando o cenário é resolvido, termina quando o resultado está em disco. Não entrar em SDDP como algoritmo de otimização.
2) As duas peças que o HPC oferece para esse padrão. Lustre: separação entre o fluxo de metadados (MDS/MDT) e o de dados (OSS/OST); a banda agregada escala com o número de OSTs. MPI-IO: no padrão desde o MPI-2; a escrita independente (MPI_File_write_at / iwrite_at) casa exatamente com este workload — offsets calculáveis, blocos contíguos por processo, ranks terminando em momentos diferentes, sem necessidade de sincronização global.
3) O anti-padrão. Concentrar a E/S em um rank escritor transforma E/S em comunicação ponto a ponto: MPI_Send do trabalhador, MPI_Recv do escritor, gravação serializada. Dois gargalos (Seção 2.6, Arquitetura atual de E/S do SDDP): o adaptador de rede do nó escritor, que recebe todos os buffers e ainda divide a NIC com o rank 0 distribuidor; e o caminho de escrita, sequencial em um só processo. Efeito colateral: atraso do escritor bloqueia os trabalhadores no Send.
4) A figura: um requisito do domínio mudou a granularidade do resultado — de 3 registros por tarefa (patamares pesado/médio/leve) para 720 (horas do mês). 240x mais dados a persistir, com a mesma computação por tarefa.

LASTRO NA DISSERTAÇÃO (se pedirem referência): descompasso entre cálculo e E/S em escala — Luu et al. 2015, Xie et al. 2020, Phillips et al. 2009; bag-of-tasks — Cirne et al. 2003; Lustre — Braam 2002 e o Operations Manual; MPI-IO — MPI-2 / MPI 5.0; escritas independentes sobre Lustre — Dickens & Logan 2008/2010, Liao et al. 2007.

SE PERGUNTAREM POR QUE A RESOLUÇÃO MUDOU: uma frase e seguir — a operação passou a exigir resolução horária para representar ponta, vales e rampas associados à variabilidade das fontes intermitentes. Não se alongar; o mérito do trabalho não depende disso.

Números de reserva: no caso avaliado (1.536 cenários x 3 estágios), 13.824 -> 3.317.760 registros.
NÃO mencionar a solução aqui — decisão do seu roteiro.

## Slide 5 — Objetivo e Contribuições

Conteúdo extraído da Seção 1.2 (Objetivos e Contribuições) da dissertação — mantém a mesma delimitação do texto.

Quatro exclusões: a construção da política (outra fase), a otimização do cálculo dentro da simulação final, a leitura dos dados de entrada e o escalonamento entre ranks.

A segunda é a mais importante de dizer em voz alta: dentro da fase escolhida, o trabalho mexe SÓ na escrita. O tempo de computação por cenário entra como dado, não como variável — por isso ele aparece praticamente constante entre as duas implementações nos gráficos do Cap. 4, e isso é esperado, não um resultado fraco.

POR QUE MOSTRAR O FORA DO ESCOPO: a delimitação isola a paralelização das escritas como variável de estudo, sem confundir os ganhos com outras frentes de otimização. Dizer isso em voz alta antecipa perguntas do tipo 'e por que não otimizaram a leitura / o escalonamento?'.

As 5 contribuições são o slide ao qual a banca mais volta na arguição — saber enunciá-las de cor.
Marcadores quadrados no padrão do modelo (Wingdings).

## Slide 6 — MPI e MPI-IO

Slide em duas colunas: à esquerda a comunicação ponto-a-ponto, à direita a E/S paralela.

ESQUERDA — protocolos Eager e Rendezvous (roteiro: 'por que eager e rendez-vous?'):
  - Eager: mensagem pequena vai direto, sem negociação — latência menor.
  - Rendezvous: mensagem grande negocia antes de transferir — controle de fluxo.
  - É essa assimetria que inspira o limiar de 128 KB entre escrita assíncrona e síncrona no Cap. 3.
  - CONFERIR o ponto de quebra: sua conclusão registra que não era 64 KB nem 128 KB.

DIREITA — escritas independentes x coletivas em MPI-IO:
  - Independente: cada rank grava sua própria região do arquivo, sem coordenação.
  - Coletiva: os ranks passam por agregadores, que reorganizam e gravam em regiões maiores.
  - A coletiva ajuda quando os acessos são pequenos e intercalados (strides); custa sincronização.
  - O SDDP tem ACESSO CONTÍGUO e offsets calculáveis, então a proposta usa escrita INDEPENDENTE — evita o custo de coordenação sem perder desempenho. Dizer isso aqui já justifica a escolha do Cap. 3.

Completar, se houver tempo: data sieving e two-phase I/O (itens do seu roteiro).

## Slide 7 — Lustre

Componentes: MDS/MDT (metadados), OSS/OST (dados), cliente.
Striping: stripe_count e stripe_size distribuem um arquivo entre OSTs. Configuração usada: stripe_count=10, stripe_size=1 MB.
MENSAGEM-CHAVE: o paralelismo do Lustre só é aproveitado se a aplicação escrever em paralelo — com um escritor único, o sistema de arquivos fica ocioso.
Se sobrar tempo, usar Lustre_striping.png como segundo slide.

## Slide 8 — Arquitetura atual de E/S do SDDP

Cada cenário resolvido envia seu bloco de resultados via MPI_Send ao rank 0, que serializa as gravações.
Dois gargalos potenciais: (1) o adaptador de rede do nó escritor, que recebe todas as transferências concorrentes; (2) o caminho de escrita serializado, que não aproveita o paralelismo do Lustre.
Roteiro (docx): cuidado com a explicação do SDDP — manter curto. Se precisar, um slide antes com cenários x estágios e o formato dos arquivos.

## Slide 9 — Arquitetura proposta com MPI-IO e Lustre

Rank 0 deixa de ser escritor: cada rank grava diretamente no Lustre via MPI-IO.
Contrastar visualmente com o slide anterior — é a mesma figura sem o funil central.

## Slide 10 — Implementação das escritas paralelas independentes

O PAR EXPLICA A IMPLEMENTAÇÃO: à direita, POR QUE a escrita independente é possível; à esquerda, COMO ela é feita. Duas ideias apenas — offset calculado e limiar de bloco. Nada mais.

DIREITA (Figura 3.4) — comece por aqui. O formato dos arquivos foi PRESERVADO, para não quebrar a cadeia de softwares do planejamento que consome as saídas. Cada registro traz estágio, cenário e hora nas três primeiras colunas; da quarta em diante, um valor por elemento do sistema elétrico (usina, reservatório, barra, interligação...). Consequência decisiva: a posição de cada registro é FUNÇÃO de (estágio, cenário, hora) — irec = posicaoLogica(...), offset = irec x tamRegistro. Nenhum processo precisa perguntar a ninguém onde escrever, e é isso que dispensa coordenação global. Os marcadores laterais são os offsets de início de cada estágio.

ESQUERDA (Código 3.1) — três decisões, na terminologia de acesso a dados do MPI-IO:
POSITIONING: offset explícito e calculado (write_at / iwrite_at), derivado do formato da direita. É o ponto central do slide.
COORDINATION: independente — sem participação dos outros ranks, o que casa com o bag-of-tasks (cada rank grava quando termina).
SYNCHRONISM: por TAMANHO DE BLOCO, e isso é DECISÃO DE PROJETO, não medida. Abaixo do limiar, MPI_File_iwrite_at (assíncrona, sobrepõe E/S e computação); acima, MPI_File_write_at (síncrona). A motivação é a mesma que rege eager x rendezvous na comunicação ponto a ponto: bloco pequeno paga latência, bloco grande paga banda.
LAYOUT (de apoio): o rank acumula em memória as horas do estágio de um cenário e só submete quando o bloco está completo — em vez de 720 escritas de uma linha, uma escrita contígua.

TAMANHO DO REGISTRO: tamRegistro = (3 + numElementos) x 4 bytes. Constante por arquivo. Exemplos da dissertação para um bloco horário de 720 horas: 1 elemento -> 4 colunas -> bloco de 11,25 KB; 10 elementos -> 13 colunas -> 36,56 KB; 300 elementos -> 303 colunas -> 852,19 KB.
USE ISSO A SEU FAVOR: é o número de elementos do sistema elétrico que decide de que lado do limiar o bloco cai. Com poucos elementos vai pelo caminho assíncrono; com 300 elementos passa de 852 KB e vai pelo síncrono. O mesmo código percorre os dois regimes conforme a base de dados — por isso a decisão é por tamanho de bloco, e não por tipo de arquivo.

OMITIDO DE PROPÓSITO — o anel de buffers. A implementação real reserva 32 buffers pré-alocados e os reutiliza de forma circular; antes de reaproveitar uma posição, o processo aguarda com MPI_Wait a conclusão da escrita anterior daquele buffer, e ao final da simulação um MPI_Waitall conclui as pendentes. Isso foi tirado do slide para não competir com o que importa. SE PERGUNTAREM 'como você garante que o buffer continua válido numa escrita não bloqueante?': é exatamente esse anel de 32 buffers; é o único ponto de bloqueio do caminho de escrita, em regime permanente quase nunca é atingido, e o custo dessas esperas foi medido e é desprezível frente ao tempo total de escrita (Seção 3.3.1).

ATENÇÃO — o limiar impresso é 128 KB. Sua anotação diz que o ponto de quebra do rendezvous não era 64 nem 128 KB. Fixe UM valor e alinhe o slide do MPI, este slide e o do tempo de bloqueio. Apresente como parâmetro de projeto; o Cap. 6 propõe varrer 64/128/256 KB.

SE PERGUNTAREM POR QUE NÃO COLETIVA: os offsets são calculáveis e os blocos contíguos, então não há o que a biblioteca agregue; a coletiva exigiria sincronizar ranks que terminam em momentos diferentes. Tentativas preliminares deram deadlock (Cap. 6).
SE PERGUNTAREM POR QUE NÃO MUDAR O FORMATO: quebraria a compatibilidade com a cadeia do planejamento; manter o formato também dá a linha de base para comparar propostas futuras de organização dos arquivos.

posicaoLogica(estagio, cenario, patamar) devolve o ÍNDICE do registro no arquivo; a fórmula explícita não está escrita no Cap. 3 — se a banca puxar esse fio, é aqui que bate.

## Slide 11 — Ambientes experimentais

PARA QUE ESTE SLIDE EXISTE: em HPC, como se mediu é cobrado tanto quanto o resultado. Ele responde de uma vez as perguntas de reprodutibilidade e prepara a leitura de todos os gráficos que vêm depois.

A FAIXA DE CIMA É O ARGUMENTO: a carga é a MESMA nos dois ambientes. Mesma base (PMO/PAR out/2023), mesmos 1.536 cenários × 3 estágios, mesmos 24 ranks por nó, mesma faixa de 2 a 32 nós. O que muda é só a infraestrutura — por isso o resultado qualitativo repetido nos dois lugares vale como portabilidade, e não como coincidência.

POR QUE 24 RANKS POR NÓ, E NÃO 48: cada rank MPI consome mais de 8 GB residentes. Com 384 GB por nó, ativar hyper-threading e dobrar os ranks estouraria a memória física. Logo, um rank por núcleo FÍSICO. É decisão imposta pela aplicação, não preferência.

STRONG SCALING, E ISSO É ESCOLHA: problema de tamanho fixo, número de nós crescente. A pergunta que interessa ao planejamento é 'o mesmo PMO roda mais rápido com mais nós?'. SE PERGUNTAREM POR WEAK SCALING: está em trabalhos futuros.

OS TRÊS CONTRASTES QUE EXPLICAM OS RESULTADOS:
1) REDE — 18,75 Gb/s de Ethernet na AWS contra 100 Gb/s de InfiniBand no SDumont. Contraintuitivo: o ambiente com a rede mais lenta é o que dá o maior ganho de banda (113x contra 13,7x). Isso reforça o diagnóstico — o gargalo da arquitetura atual não é a rede em si, é a serialização no nó escritor.
2) OSTs — 10 na AWS contra 6 no SDumont. A banda agregada do Lustre escala com o número de OSTs, o que já antecipa parte da diferença de magnitude entre os dois ambientes e conecta com o slide do efeito dos OSTs.
3) DEDICADO x COMPARTILHADO — este é o mais importante. O FSx da AWS é exclusivo do experimento; o Lustre do SDumont divide banda e metadados com outros jobs. O SDumont é, portanto, o cenário ADVERSO — e é justamente por preservar a vantagem lá que a solução se mostra portátil.

SE PERGUNTAREM PELA BANDA PERCEBIDA DE 60,5 Gb/s EM 2 NÓS NA AWS, acima dos 18,75 Gb/s nominais do adaptador: é consequência da definição da métrica. Em 2 nós, cerca de metade dos trabalhadores fica no mesmo nó do escritor e comunica por memória compartilhada, com bloqueio mínimo; o denominador encolhe. Conforme cresce a escala, a fração de envios locais cai (um quarto em 4 nós, um oitavo em 8, menos de 6% em 16) e a métrica converge para muito abaixo do nominal.

PENDÊNCIA — COMPILADOR E FLAGS: a avaliação de banca marcou como risco alto a ausência de compilador, flags de otimização e configuração do mpirun. Esses dados não estão no Capítulo 4; sem eles, este slide fica incompleto no critério de reprodutibilidade. Acrescente uma linha em cada coluna assim que levantar os valores.

## Slide 12 — Caracterização do perfil de E/S

As duas figuras juntas formam o argumento — separadas, cada uma conta metade da história.

ESQUERDA (4.1): predominância de requisições PEQUENAS. É o que torna o workload hostil ao Lustre e o que justifica o limiar de 128 KB no Cap. 3.

DIREITA (4.2): o VOLUME se concentra nos blocos maiores.

A LEITURA CONJUNTA: a maior parte das operações é pequena, mas a maior parte dos bytes está em poucas operações grandes. Ou seja, o custo não é proporcional ao volume — são as muitas requisições pequenas que pagam o custo fixo de coordenação. É exatamente por isso que faz sentido tratar os dois regimes de forma diferente (assíncrono para pequenos, síncrono para grandes).

Conclusão do seu docx: não é vantajoso ter muitos arquivos pequenos, por causa da operação coletiva — agrupar resultados menores. Liga direto com o trabalho futuro de reorganizar os arquivos diários.

## Slide 13 — Banda agregada — AWS

UM SLIDE COM ANIMAÇÃO. Abre só com a implementação atual; ao CLICAR, as barras do MPI-IO aparecem com fade. São duas imagens sobrepostas no mesmo retângulo — a de cima ('MPI-IO (animar)') tem fundo transparente e só contém as barras hachuradas mais a entrada da legenda.

COMEÇAR OS EXPERIMENTOS POR AQUI (decisão do seu roteiro).

ANTES DO CLIQUE — mensagem: a banda não cresce com o número de nós, ela CAI. De 60,5 Gb/s em 2 nós para 3,4 Gb/s em 32 nós. Dobrar o hardware piora a banda percebida pela aplicação. Deixe a plateia absorver isso antes de clicar.
O eixo y vai até 470 Gb/s com espaço vazio acima: é de propósito, é onde o MPI-IO vai entrar.

DEPOIS DO CLIQUE: em 32 nós, 380,3 contra 3,4 Gb/s = 113x mais banda, e o sentido da curva se inverte — o MPI-IO cresce com os nós (57,0 / 106,0 / 167,0 / 274,2 / 380,3).
Em 2 nós as duas são equivalentes (60,5 contra 57,0) e a atual é levemente melhor. DIZER ISSO: o ganho aparece com escala, não em qualquer regime — e o Cap. 6 precisa registrar isso.

SE APRESENTAR NO GOOGLE APRESENTAÇÕES: a animação é descartada na importação e as duas séries aparecem juntas de saída. Nesse caso use o arquivo de reserva Apresentacao_esqueleto_banda_2slides.pptx, ou recrie a animação em Inserir > Animação > Aparecer, 'ao clicar', na imagem 'MPI-IO (animar)'.

## Slide 14 — Tempo de execução — AWS

ANIMAR: a imagem 'MPI-IO (animar)' deve receber entrada Aparecer, ao clicar.

ANTES DO CLIQUE — só a implementação atual. Números: 8.971 s em 2 nós, caindo até 1.874 s em 16 nós, e SUBINDO para 2.013 s em 32 nós. A regressão é significativa: IC 95% não se sobrepõem (1.874 ± 71 contra 2.013 ± 36). Em 32 nós a E/S é 49,5% do tempo.
Deixe a plateia ver que dobrar de 16 para 32 nós PIORA o tempo antes de clicar.

DEPOIS DO CLIQUE — MPI-IO: 1.274 s em 32 nós, 1,58x mais rápido, e continua escalando de 16 para 32. A E/S cai de 49,5% para 0,7%.
ASSUMA A RESSALVA: em 32 nós há apenas 2 cenários por rank, então parte da perda de eficiência é granularidade. Sua defesa: a fração de E/S é medida e instrumentada, não inferida por resíduo.
Novo limite visível: MPI_File_open/close chega a 11,6% do tempo em 32 nós.

--- nota anterior ---
USAR A VERSÃO EM ANIMAÇÃO (Tempo_execucao_AWS_transicao_2slides.pptx): primeiro só a implementação atual, depois o MPI-IO aparece.
Números: 8.971 s em 2 nós → 1.874 s em 16 nós → 2.013 s em 32 nós (PIORA 7,4%; IC 95% não se sobrepõem).
Em 32 nós a E/S é 49,5% do tempo. Com MPI-IO: 1.274 s (1,58x mais rápido), E/S cai para 0,7%.
ASSUMIR A RESSALVA: em 32 nós há só 2 cenários por rank — parte da perda é granularidade. Defesa: a fração de E/S é medida, não inferida.

## Slide 15 — AWS — implementação atual

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

A CURVA VIRA: o tempo total cai até 16 nós (1.873,56 s) e PIORA em 32 (2.013,06 s). É o regime saturado do escritor único.
A banda percebida desaba de 60,51 para 3,37 Gb/s, mais de uma ordem de grandeza, enquanto a fração de E/S sobe de 0,34% para 49,51%.
A eficiência cai a 27,9% em 32 nós. Speedup máximo de 4,79x, em 16 nós.
Os 60,51 Gb/s em 2 nós excedem os 18,75 Gb/s nominais do adaptador: em 2 nós metade dos trabalhadores comunica por memória compartilhada com o escritor, e o denominador da banda percebida encolhe (definição na Seção 3.5).

## Slide 16 — AWS — implementação MPI-IO

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

MONOTÔNICA NOS DOIS SENTIDOS: o tempo total cai em toda a faixa (8.858,91 -> 1.274,25 s) e a banda cresce sem inflexão (57,04 -> 380,30 Gb/s). O armazenamento não saturou.
A E/S deixa de ser fator: fica em 0,70% do tempo em 32 nós, com tempo absoluto praticamente constante (18,98 -> 8,96 s).
A coluna nova é o open/close: 42,48 s em 2 nós para 147,26 s em 32. Cresce com o número de nós porque é operação coletiva, mas é UMA por execução — não cresce com cenários nem com estágios. Os 11,6% de participação em 32 nós estão inflados porque o teste tem só 3 estágios mensais.
Eficiência de 43,5% em 32 nós: gargalo de computação em strong scaling, não de E/S.

## Slide 17 — AWS — comparativo atual × MPI-IO

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

ESTA É A TABELA QUE RESUME O EXPERIMENTO AWS. Leia a coluna 'Ganho de banda': 0,94x, 2,07x, 8,82x, 60,66x, 113,00x. O ganho é de ESCALA.
O tempo total melhora 36,7% em 32 nós; a E/S melhora 99,1%.
ASSUMA O PONTO FRACO: em 4 nós há PIORA de 6,3% no tempo total, apesar de a banda já ser 2,07x melhor. O Cap. 6 registra como investigação pendente e atribui a fatores externos ao módulo de E/S — provavelmente variação do tempo de computação entre repetições.
Em 2 nós o empate (1,3%) é esperado: o escritor ainda não saturou e o custo fixo da camada MPI-IO pesa.

## Slide 18 — Efeito do número de OSTs no Lustre

Experimento de sensibilidade: 4 OSTs contra 10 OSTs, com TODOS os demais parâmetros constantes — mesma base PMO/PAR de outubro de 2023, 1.536 cenários, 3 estágios mensais, 24 ranks por nó e mesma instrumentação MPI-IO. Rodada dedicada, portanto os valores absolutos são diretamente comparáveis.

ESQUERDA (4.7): a banda agregada percebida pela aplicação — o EFEITO.
DIREITA (4.6): o tempo de envio por classe de tamanho de mensagem — a CAUSA.

Ordem alinhada ao seu roteiro, que manda começar pela banda: primeiro o resultado que interessa (mais OSTs, mais banda), depois o mecanismo que o explica (as requisições se distribuem entre mais servidores de objeto e o tempo por operação cai). É a evidência que sustenta a contribuição de 'orientações para o dimensionamento do sistema de arquivos'.

PENDÊNCIA: a avaliação de banca apontou a Subseção 4.1.4 (OSTs) como estruturalmente anômala no texto — vale reposicionar no capítulo, embora no slide o par funcione bem aqui.
A configuração de 10 OSTs é a mesma do Experimento AWS principal; stripe_count=10 e stripe_size=1 MB ainda carecem de justificativa quantitativa no texto (outra pendência mapeada).

## Slide 19 — Banda agregada — SDumont

ANIMAR: a imagem 'MPI-IO (animar)' deve receber entrada Aparecer, ao clicar.

AMBIENTE DIFERENTE: nunca comparar com a AWS lado a lado — hardware, rede e Lustre distintos (aqui o Lustre é compartilhado). Apresentar como verificação de PORTABILIDADE do comportamento, não como comparação de desempenho.

ANTES DO CLIQUE — a atual cai de 27,9 Gb/s em 2 nós para 2,5 Gb/s em 32 nós. Mesmo padrão da AWS.
Note as barras de erro largas em 2, 4 e 8 nós: é Lustre compartilhado com outros usuários, e essa variabilidade é esperada. Se perguntarem, essa é a resposta.

DEPOIS DO CLIQUE — MPI-IO cresce com os nós: 5,5 / 8,9 / 12,1 / 18,9 / 34,1 Gb/s. Em 32 nós, 34,1 contra 2,5 = 13,6x. O sentido da curva se inverte, como na AWS.
Em 2, 4 e 8 nós a atual é MELHOR que a MPI-IO neste ambiente — dizer isso. O ganho aparece a partir de 16 nós, e é o Cap. 6 que precisa registrar essa ressalva.

--- nota anterior ---
AMBIENTE DIFERENTE: nunca comparar AWS e SDumont lado a lado — parâmetros e hardware distintos. Apresentar como verificação de portabilidade do comportamento, não como comparação de desempenho.

## Slide 20 — Tempo de execução — SDumont

ANIMAR: a imagem 'MPI-IO (animar)' deve receber entrada Aparecer, ao clicar.

ANTES DO CLIQUE — a atual: 14.524 s em 2 nós, decresce até 3.130 s em 16 nós e volta a subir para 3.744 s em 32 nós. Mesma inversão observada na AWS, em hardware completamente diferente.
MENSAGEM CENTRAL DO SLIDE: o gargalo não é artefato de um ambiente específico.

DEPOIS DO CLIQUE — MPI-IO: 2.519 s em 16 nós e 2.233 s em 32 nós, ainda escalando. Em 32 nós, 3.744 contra 2.233 = 1,68x mais rápido.
Em 2 e 4 nós as duas praticamente empatam (14.524 contra 14.796; 7.758 contra 7.800), com leve vantagem da atual — mesma ressalva da AWS.

Dados: pasta 'Sem rede' (atual) e 'Sem rede - MPIO - ASYNC' (MPI-IO). Existe também uma pasta ASYNC-FIX com números melhores em 32 nós (1.808 s) que NÃO é a usada nas figuras da dissertação — não citar para não gerar inconsistência.

--- nota anterior ---
Mesmo padrão qualitativo: decresce até 16 nós e perde eficiência rapidamente nas maiores escalas (14.524 s em 2 nós).
Mensagem: o gargalo não é artefato de um ambiente específico.

## Slide 21 — SDumont — implementação atual

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

MESMO PADRÃO, OUTRA ESCALA: o tempo cai até 16 nós (3.129,98 s) e piora em 32 (3.743,71 s). O colapso aqui começa em 16 nós, não em 8 como na AWS.
Banda de 27,86 para 2,49 Gb/s; fração de E/S de 0,55% para 45,83%; eficiência de 100% para 24,2%.
A banda de partida é bem menor que na AWS (27,86 contra 60,51 Gb/s) porque o Lustre é COMPARTILHADO com outros jobs e tem 6 OSTs, não 10.
O tempo de comunicação é alto e quase constante (370 a 545 s) — é o custo de mover tudo até o rank escritor.

## Slide 22 — SDumont — implementação MPI-IO

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

Tempo total decrescente em toda a faixa (14.796 -> 2.233 s) e banda monotonicamente crescente (5,55 -> 34,10 Gb/s), como na AWS.
O tempo médio de E/S por processo cai de 321,24 s para 64,06 s, e a fração de E/S fica abaixo de 5% em todas as configurações.
ATENÇÃO À PRIMEIRA LINHA: 5,55 Gb/s em 2 nós é MENOS que os 27,86 Gb/s da implementação atual. Em pequena escala, com 6 OSTs e um sistema de arquivos disputado, a escrita distribuída não compensa o custo fixo. A partir de 8 nós inverte.
O open/close chega a 230,03 s em 32 nós — mais que na AWS, coerente com um sistema de arquivos compartilhado e mais lento em metadados.

## Slide 23 — SDumont — comparativo atual × MPI-IO

SLIDE DE BACKUP — tabela completa do Capítulo 4, para a arguição.

A TABELA MAIS DELICADA DAS SEIS, E A MAIS HONESTA. Ela mostra o ganho de 40,4% em 32 nós e, ao mesmo tempo, os números negativos em pequena escala.
ESPERE A PERGUNTA sobre o −305,3% de E/S em 2 nós. Resposta: são métricas de agregação diferente — na implementação atual a coluna é o tempo de E/S do rank escritor; na MPI-IO é o tempo MÉDIO de E/S por processo, que passa a existir em todos os ranks. Em 2 nós, com 6 OSTs e Lustre compartilhado, esse tempo por processo é grande; a partir de 8 nós a soma dos ganhos inverte o sinal (7,7%, 87,3%, 96,3%).
Não fuja da linha de 2 e 4 nós: dizer 'em pequena escala a arquitetura atual é competitiva, o ganho é de escala' é mais forte do que ser confrontado com isso.
O teto de 34,10 Gb/s contra os 380,30 Gb/s da AWS é o argumento do trabalho futuro de sistema de arquivos ad-hoc (Expand).

## Slide 24 — Trabalhos relacionados

PARA QUE ESTE SLIDE EXISTE: a avaliação de banca de junho deu 0,0 ao Cap. 5 e apontou a ausência de trabalhos relacionados como risco crítico. Este slide responde 'onde você se posiciona?' — a terceira coluna é o slide; as duas primeiras são contexto.

A ORDEM É UM ARGUMENTO, em três passos:
1) DICKENS & LOGAN (2008) é o trabalho que introduziu o uso de MPI-IO sobre o Lustre e caracterizou o desempenho dessa combinação. Ele entra aqui por uma razão simples e forte: é o MESMO conjunto de ferramentas deste trabalho — MPI-IO sobre Lustre, em ambiente HPC. O SDDP é um novo caso de uso dessa mesma pilha. Não é preciso ir além disso no slide.
2) LIAO et al. (2007) dá o mecanismo de alinhamento. Dois estágios: o local agrega mensagens por destino (utilização de rede); o global mantém páginas do tamanho da stripe, cada uma com um dono, o que faz toda escrita ao sistema de arquivos nascer alinhada e elimina o falso compartilhamento de locks. DIFERENÇA: o efeito do 1º estágio já é obtido aqui pela agregação das 720 horas por (estágio, cenário); o 2º não foi implementado. RESSALVA HONESTA, se perguntarem: o alinhamento deles vem da POSSE das páginas, não só do corte nas fronteiras — replicar isso exigiria reintroduzir uma noção de dono por stripe, ou seja, a coordenação que a arquitetura proposta evita.
3) GARCÍA-CARBALLEIRA et al. (2023) muda a camada, não a aplicação. Volume efêmero sobre o armazenamento local dos nós alocados ao job, com stage-in/stage-out. DIFERENÇA: é o único dos três que ataca a contenção EXTERNA — a que impôs o teto de 34,1 Gb/s no SDumont, uma ordem de grandeza abaixo dos 380,3 Gb/s da AWS dedicada. Não compete com a proposta: compõe com ela.

FRASE DE FECHAMENTO DO SLIDE: os três sustentam a escolha de MPI-IO sobre Lustre. Dickens caracteriza o desempenho dessa pilha, Liao muda a bufferização, García-Carballeira muda a camada de armazenamento — e este trabalho muda quem escreve, sem sair do padrão MPI-IO e sem alterar o formato dos resultados.

SE PERGUNTAREM POR MAIS TRABALHOS: o Cap. 5 tem seis (estes três, mais Dickens & Logan 2010 com a Y-lib, Gropp 2008 e Liao 2008). Gropp 2008 é o lastro teórico da escolha: com acessos non-interleaved, MPI_File_write_all degenera em MPI_File_write mais o custo de sincronização — logo, a coletiva é estritamente pior nesse regime. Dickens & Logan 2010 mostra que agregar em poucos processos pode ser o pior caminho no Lustre.

LACUNA CONHECIDA, se alguém perguntar por que não HDF5 ou ADIOS: essas bibliotecas trazem portabilidade e autodescrição de formato, e é exatamente o formato binário que precisa ser preservado para não quebrar a cadeia de softwares do planejamento. Vale acrescentar essa família ao Cap. 5.

(Posição provisória: antes das Conclusões, espelhando a ordem da dissertação. Considere mover para depois do slide do Lustre — apresentado ANTES da arquitetura proposta, ele justifica a escolha antes de a pergunta nascer.)

## Slide 25 — Conclusões

ATENÇÃO — pendências que você mesmo anotou no docx:
1) 'Erro grave nas conclusões: decorrente da saturação do adaptador de rede do processo escritor único' — corrigir a redação.
2) A quebra do rendezvous não era em 64 KB nem em 128 KB — acertar o número (toca os slides 5, 9 e 13).
3) Validação dos dados com softwares existentes.

ORIGEM DE CADA NÚMERO (Cap. 4):
1) Banda atual AWS: 60,5 Gb/s em 2 nós -> 18,9 (8) -> 4,5 (16) -> 3,4 (32). Total atual: 1.873,56 s em 16 nós contra 2.013,06 s em 32 — a curva vira. Diga 'inverte a escalabilidade': adicionar nós piora.
2) Fração de E/S da atual: 7,6% (8 nós) -> 28,2% (16) -> 49,5% (32). MPI-IO fica <= 1% a partir de 4 nós; 0,70% em 32. Total 2.013,06 -> 1.274,25 s (36,7%; 1,58x). Redução do tempo de E/S: 99,1%.
3) Banda MPI-IO AWS: 57,0 -> 106,0 -> 167,0 -> 274,2 -> 380,3 Gb/s (113,00x em 32). SDumont: 5,5 -> 34,1 Gb/s (13,7x). Monotônica nos dois: o teto do armazenamento não foi atingido.
4) SDumont: pequeno sobrecusto em 2 e 4 nós (1,9% e 0,5%), ganho a partir de 8 nós (0,3%, 19,5% e 40,4%). Redução do tempo de E/S: 96,3%. Lustre COMPARTILHADO, com concorrência de outras cargas — por isso a portabilidade é o resultado mais robusto.
5) OSTs (AWS): 4 -> 10 OSTs amplia a banda ~5,6x em 16 nós e ~23,6x em 32. Mensagem: stripe_count e stripe_size são parâmetro de projeto, não detalhe operacional.
6) Eficiência em 32 nós: 43,5% (AWS) e 41,4% (SDumont). É strong scaling: problema fixo, cada rank resolve menos cenários, custos ~constantes de computação (acesso à memória) deixam de ser amortizados — gargalo COMPUTACIONAL, distinto do de E/S. MPI_File_open/close: 42 s em 2 nós -> 147 s em 32; uma chamada por execução, independe do número de cenários e estágios; a fração de 11,6% está inflada porque o teste tem só 3 estágios mensais.

SE PERGUNTAREM 'e em 2 e 4 nós?': a atual é competitiva ou melhor (na AWS, -6,3% em 4 nós) porque o escritor ainda não saturou e o custo fixo da MPI-IO pesa. O ganho é de escala — e é justamente onde o problema real vive.

## Slide 26 — Trabalhos futuros

Extraído do Capítulo 6. Manter curto: a banca lê o slide. Ordem proposta: primeiro o que refina a solução entregue, depois o que a estende.

1) Dos 117 arquivos de resultado, 104 são horários e 13 diários; os diários respondem por TODAS as escritas de blocos muito pequenos, porque a aplicação não agrupa os dias (nos horários ela agrupa as 720 horas em uma escrita). A escrita assíncrona mitiga em parte, mas a frequência de requisições pequenas ao Lustre permanece.
2) Liao et al. (2007): bufferização em dois estágios alinhada ao particionamento do sistema de arquivos melhora escritas pequenas e desalinhadas. Objetivo: uma submissão MPI-IO por stripe, logo um OST por requisição, reduzindo contenção entre ranks sobre o mesmo OST.
3) O limiar síncrono/assíncrono adotado é parâmetro de projeto, não medida — daí a proposta de varrer 64/128/256 KB. Cuidado: alinhar com o valor citado nos slides 5, 9 e 13.
4) ESTE É O ITEM DE DEFESA para 'por que não escrita coletiva?'. Tentativas preliminares deram deadlock, atribuído a múltiplas escritas por cenário combinadas ao desalinhamento do número de cenários por rank no bag-of-tasks. Viabilizar exigiria sincronização que reconcilie distribuição dinâmica de tarefas com a semântica coletiva.
5) Redes: EFA/InfiniBand para ver até que ponto a rede deixa de limitar e como escala o custo da coordenação MPI-IO em baixa latência. Escala: acima de 32 nós podem aparecer saturação de metadados e efeitos de coordenação coletiva.
6) Fase de geração de cortes: padrão de comunicação e sincronização diferente do da simulação final. Gargalo computacional: profiling da hierarquia de memória, para separar efeitos de computação e de E/S na eficiência paralela.

SE PERGUNTAREM POR WEAK SCALING: o estudo é deliberadamente strong scaling (caso fixo, nós variáveis), porque a pergunta de negócio é 'o mesmo PMO roda mais rápido com mais nós?'. Weak scaling entra aqui, como continuidade.

Limitação operacional, se perguntarem: a disponibilidade de instâncias r7i.12xlarge na AWS restringiu a janela de experimentação.

## Slide 27 — Tempo de bloqueio dos envios por tamanho — AWS

Roteiro (docx): 'tempo de bloqueio dos blocos'.
Aqui aparece a transição eager/rendezvous. CONFERIR o ponto de quebra — sua conclusão diz que não era 64 KB nem 128 KB.

## Slide 28 — Tempo de bloqueio dos envios por tamanho — SDumont

Fecha a caracterização no segundo ambiente.
