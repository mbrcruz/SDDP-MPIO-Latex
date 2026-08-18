# Avaliação da apresentação de defesa — 2ª rodada

**Arquivo:** `Apresentacao_esqueleto.pptx` — 20 slides, 4 com animação
**Escopo desta avaliação:** a **defesa de mestrado**. O slide do gancho (nº 3, LineShine/SHOTGUN) está **fora de escopo** — ele será usado apenas no ensaio na empresa. Contando a capa antiga (nº 2, oculta) e o gancho como fora, a defesa tem **17 slides visíveis**.
**Data:** 18/08/2026 · **Referência:** avaliação anterior (`Avaliacao_apresentacao.md`), nota global ≈ 7,3
**Critério:** o que uma banca do PESC/COPPE, com formação em HPC, tende a cobrar de uma dissertação sobre escalabilidade de E/S.

---

## 1. Veredito

A apresentação melhorou onde mais pesava: **o enquadramento da abertura** e **o fecho**. O deck conta hoje uma história defensável de ponta a ponta — descompasso cálculo × E/S, carga bag-of-tasks, o que o HPC oferece, por que o escritor único desperdiça, como a proposta funciona, o que os dois ambientes mostram, o que se assume como limite.

O que trava a nota não é mais a narrativa: são **três defeitos visuais concretos** (títulos estourando) e **duas ausências estruturais** — trabalhos relacionados e metodologia experimental.

Sair do gancho ainda ajuda em dois pontos: a defesa passa a abrir direto no terreno técnico, que é o mais seguro para uma banca de computação, e libera um tempo de fala.

| Bloco | Slides | Antes | Agora | Comentário |
|---|---|---|---|---|
| Abertura e motivação | 1, 4–5 | 8,5 | 8,5 | Introdução muito mais afiada; capa nova perdeu orientador e banca |
| Fundamentação | 6–7 | 7,5 | 7,5 | Inalterada; ainda sem o "por que não HDF5/ADIOS" visível |
| Proposta | 9–10 | 8,5 | 8,5 | O slide 10 ganhou profundidade e perdeu a animação em 5 passos |
| Resultados | 11–18 | 8,0 | 8,0 | Inalterados; faltam metodologia e placar consolidado |
| Fecho | 19–20 | 6,0 | **8,0** | Quantificado, com limites assumidos e o item da coletiva |
| Cobertura (o que não existe) | — | 4,5 | **5,0** | O slide 10 cobriu implementação; o resto continua faltando |
| **Global** | | **7,3** | **≈ 7,8** | Boa apresentação; o que resta é pontual e conhecido |

---

## 2. O que melhorou desde a última avaliação

**A introdução virou um argumento de HPC em três passos.** Carga de trabalho (bag-of-tasks, bloco contíguo por par estágio/cenário) → o que a infraestrutura oferece (banda agregada que cresce com OSTs, MPI-IO escrevendo em offsets distintos) → por que isso não se realiza (escritor único converte E/S em comunicação ponto a ponto). Cada afirmação tem lastro no Cap. 1 ou 2. É difícil interromper essa sequência com uma objeção. Sem o gancho antes dela, ela também passa a ser a primeira impressão da banca — e sustenta bem esse papel.

**As Conclusões deixaram de ser qualitativas.** Banda caindo de 60,5 para 3,4 Gb/s, o melhor tempo da AWS em 16 e não em 32 nós, 49,5% → 0,7% de E/S, 113× e 13,7× nos dois ambientes, 5,6× e 23,6× com OSTs. E, o que mais conta numa banca, **os limites assumidos por você mesmo**: eficiência de 43,5% em 32 nós como gargalo de computação, e o `MPI_File_open/close` requalificado como custo fixo por execução em vez de "novo limite".

**Trabalhos futuros agora responde à pergunta que ia vir.** O item da escrita coletiva com o *deadlock* é a resposta pronta para "por que não two-phase I/O?", que antes vivia só nas notas do slide de MPI.

**O slide 10 fechou um vazio real.** Antes o deck afirmava "offsets pré-calculados" sem mostrar de onde sai o cálculo. Agora a figura do formato preservado justifica que a posição é função de (estágio, cenário, hora), e o pseudocódigo mostra a derivação — `irec` → `offset` → `tamBloco`. É o slide que sustenta a frase "dispensa coordenação global".

**As notas do apresentador estão em outro nível.** Slide 10 com 3.907 caracteres, Conclusões com 2.020, Trabalhos futuros com 2.059, com a origem de cada número e respostas pré-formuladas.

---

## 3. Defeitos que aparecerão no projetor

### 3.1 Três títulos estouram para duas linhas e cobrem o subtítulo

O placeholder de título comporta ~42 caracteres em uma linha. Acima disso a segunda linha desce sobre o subtítulo — no slide 10 ela cobre "Capítulo 3 — Código 3.1 (esq.) e Figura 3.4 (dir.)", e no 14 cobre "Capítulo 4 — Figura 4.5".

| Slide | Título | Caracteres |
|---|---|---|
| 10 | Implementação das escritas paralelas independentes | 50 |
| 14 | Tempo de bloqueio dos envios por tamanho — AWS | 46 |
| 18 (oculto) | Tempo de bloqueio dos envios por tamanho — SDumont | 50 |

Sugestões que cabem: "Implementação das escritas independentes" (39), "Tempo de bloqueio por tamanho — AWS" (35). Correção de 5 minutos, e é a primeira coisa que a banca vê.

### 3.2 A capa perdeu orientador e banca

O slide 1 traz apenas seu nome e a data. Orientador e banca estavam na capa antiga, hoje oculta no slide 2. Numa defesa isso não é detalhe de estilo: a capa é o registro formal do ato.

Dois reparos no mesmo slide: **"da Escrita Serializada as Escritas Paralelas"** pede **"às"**; e a quebra manual de linha corta o título em "…da Escrita / Serializada as Escritas Paralelas…", separando o substantivo do adjetivo. Quebrar depois de "HPC:" resolve.

### 3.3 O limiar de bloco aparece com duas histórias diferentes

O slide 10 apresenta os 128 KB como **decisão de projeto** — leitura honesta, coerente com o Cap. 6, que propõe varrer 64/128/256 KB. Mas as notas do slide 11 dizem que o perfil de requisições pequenas "justifica o limiar de 128 KB", o que soa **empírico**, e as notas dos slides 6 e 14 mandam "conferir o ponto de quebra". São três versões do mesmo número.

Hoje ele está escrito em cinco lugares: corpo do slide 10 (dentro do pseudocódigo), corpo do slide 20 (64/128/256 KB) e notas dos slides 6, 11 e 14. Escolha uma frase — *a assimetria eager/rendezvous motivou usar um limiar; o valor foi adotado como parâmetro de projeto e não calibrado* — e repita a mesma frase nos cinco pontos.

### 3.4 O slide 14 é o elo fraco dos resultados

Quatro gráficos num grid 2×2, ilegíveis em projeção; 167 caracteres de nota; e é justamente o slide onde vive a questão do ponto de quebra. Pior: o equivalente do SDumont (slide 18) está **oculto**, o que quebra a simetria AWS × SDumont que sustenta o argumento de portabilidade. Ou os dois entram, ou os dois vão para backup — e a segunda opção é mais defensável, porque a portabilidade já está demonstrada pelos slides de banda e de tempo nos dois ambientes.

### 3.5 Inconsistências de forma, pequenas mas visíveis

- **Slide 5** é o único slide de conteúdo com o subtítulo **vazio**. É também o mais denso do deck: nove itens em três blocos a 12 pt sobre colunas de 6,1 in — no limite do legível a distância.
- **Slide 6** é o único que põe a referência do capítulo **no pé** do slide; todos os outros usam o placeholder de subtítulo, no alto.
- **Slide 7 (Lustre)** não tem referência de capítulo nenhuma.

---

## 4. O que continua não existindo

Os dois itens abaixo já estavam na avaliação anterior, com a mesma severidade. Nenhum foi endereçado.

**4.1 Nenhum slide de trabalhos relacionados.** A avaliação de banca de junho deu 0,0 ao Cap. 5 e apontou isso como risco crítico nº 1. Os trabalhos já estão citados nas suas notas — Dickens & Logan (2008, 2010), Liao *et al.* (2007), ROMIO/*data sieving*, Kang (2020), Xie (2020), Luu (2015). Falta o slide com 4–6 deles e uma coluna de "o que este trabalho faz de diferente".

**4.2 Nenhum slide de metodologia experimental.** O setup está espalhado nas notas. Em HPC, *como* se mediu é escrutinado tanto quanto o resultado: hardware dos dois ambientes (r7i.12xlarge; nós do SDumont), rede, `stripe_count=10` e `stripe_size=1 MB`, número de OSTs, o caso (1.536 cenários × 3 estágios mensais, 24 ranks/nó), 5 repetições com IC 95%, e — item marcado como risco alto na avaliação de banca — **compilador, flags e configuração do `mpirun`**. É também onde se nomeia o regime como **strong scaling**, antes que alguém pergunte por *weak scaling*.

**4.3 Sem placar consolidado e sem bloco de backup.** As Conclusões citam números que a plateia nunca viu numa tabela. E uma defesa se decide muitas vezes na arguição: valem no backup as tabelas completas do Cap. 4, o setup detalhado, os slides 14/18 recolhidos, as 5 imagens do fluxo de decisão (`fluxo_passo1..5.png`, ainda na pasta) e a rodada `ASYNC-FIX` do SDumont — que existe, tem 1.808 s contra 2.233 s em 32 nós e **não** é a usada nas figuras.

---

## 5. Uma perda a considerar

O slide do **fluxo de decisão da escrita independente** (Figura 3.3), com a construção em 5 passos, foi substituído pelo slide 10. A troca faz sentido — o pseudocódigo mostra mais e o offset ficou explícito —, mas o deck perdeu a única explicação *visual* da bifurcação por tamanho de bloco, que agora vive num comentário de uma linha dentro do código. No bloco de backup, aquele slide é o lugar natural para receber a pergunta "como exatamente você decide entre síncrono e assíncrono?". As imagens estão preservadas na pasta.

---

## 6. Tempo

17 slides visíveis + 4 cliques de animação ≈ **21 tempos de fala**. Para 30–40 minutos, 1,4 a 1,9 minuto por tempo — confortável. Entrando os três slides recomendados (relacionados, metodologia, placar), vai a 24 tempos, ou 1,25–1,7 min cada, o que continua viável **sem** precisar cortar nada. Recolher os slides 14 e 18 para backup deixa de ser necessidade de tempo e passa a ser só a decisão de coerência da seção 3.4.

---

## 7. Prioridade

| # | Ação | Esforço | Impacto |
|---|---|---|---|
| 1 | Encurtar os títulos dos slides 10, 14 e 18 | 5 min | Alto |
| 2 | Orientador e banca na capa; "às"; quebra de linha | 5 min | Alto |
| 3 | Fixar uma única frase para o limiar nos 5 pontos | 20 min | Alto |
| 4 | Slide de metodologia experimental e reprodutibilidade | 1 h | Alto |
| 5 | Slide de trabalhos relacionados | 2–3 h | Alto |
| 6 | Ocultar o slide 3 (gancho) na versão da defesa | 1 min | Médio |
| 7 | Slide-placar com o resumo quantitativo | 1 h | Médio |
| 8 | Recolher 14 e 18 para backup (resolve a assimetria) | 10 min | Médio |
| 9 | Subtítulo no slide 5; referência de capítulo no 6 e no 7 | 10 min | Baixo |
| 10 | Bloco de backup (tabelas, setup, fluxo em 5 passos, ASYNC-FIX) | 1–2 h | Médio |

Os itens 1, 2, 3, 6 e 9 somam menos de uma hora e eliminam tudo que é visível ou incoerente. Os itens 4 e 5 são os que mudam a nota.

---

## Anexo — a versão de ensaio na empresa

Para a plateia da empresa, o gancho é um ativo, não um risco: ela conhece o SDDP e a pergunta "o que aconteceria com 10.000 cenários e 120 estágios em 13,79 milhões de cores?" prende atenção. Duas observações válidas **só** para essa versão:

- **Ali o laço precisa fechar.** A plateia registra a pergunta e vai perceber se ela não voltar. E você tem a resposta na escala da pergunta: paralelismo não falta — na arquitetura atual a banda percebida **cai** de 60,5 para 3,4 Gb/s ao ir de 2 para 32 nós, e o melhor tempo acontece em 16. Escalar cores não resolve; escalar o caminho de escrita resolve. Um slide espelhando o layout do slide 3, ao final.
- **Mantenha um arquivo só, com o slide 3 oculto.** Ocultar e reexibir é um clique, e evita duas versões divergindo — que é como se perde uma correção de última hora.
