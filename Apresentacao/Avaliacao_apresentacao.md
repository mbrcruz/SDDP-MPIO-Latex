# Avaliação da apresentação de defesa — lente de banca de mestrado em HPC

**Arquivo avaliado:** `Apresentacao_esqueleto.pptx` — 19 slides (17 visíveis, 1 oculto), 4 slides com animação
**Data:** 17/08/2026
**Critério:** o que uma banca do PESC/COPPE, com formação em computação de alto desempenho, tende a cobrar de uma dissertação sobre escalabilidade de E/S.

---

## 1. Veredito

A apresentação tem **espinha dorsal sólida e narrativa acima da média**: o problema é enquadrado em HPC, o diagnóstico precede a proposta, a evidência vem de dois ambientes e os limites são assumidos. O que falta não é qualidade do que está lá — é **cobertura**. Três blocos que uma banca de HPC espera encontrar não têm slide: trabalhos relacionados, metodologia experimental e o fechamento do gancho de abertura.

**Nota estimada por bloco** (peso subjetivo, escala 0–10):

| Bloco | Slides | Nota | Comentário |
|---|---|---|---|
| Abertura e motivação | 1–4 | 8,5 | O 240× é um gancho forte e ancorado em dado |
| Fundamentação | 5–7 | 7,5 | Correta e enxuta; falta o "por que não HDF5/ADIOS" |
| Proposta | 8–9 | 8,5 | O fluxo em 5 etapas é o melhor slide do deck |
| Resultados | 10–17 | 8,0 | Fortes; faltam metodologia e um placar consolidado |
| Fecho | 18–19 | 6,0 | Conclusões boas, mas o gancho fica sem resposta |
| Cobertura (o que não existe) | — | 4,5 | Sem trabalhos relacionados, sem setup, sem backup |
| **Global** | | **≈ 7,3** | Boa apresentação com lacunas estruturais corrigíveis |

---

## 2. O que está forte — e por quê

**O enquadramento em HPC, não no setor elétrico.** O slide 3 abre pelo descompasso entre capacidade de cálculo e de E/S, apresenta o sistema de arquivos paralelo e só então introduz o SDDP como *carga de trabalho* bag-of-tasks. Para uma banca de computação, esse é o terreno certo — e reduz a exposição a perguntas de domínio energético.

**A motivação é quantitativa, não retórica.** "3 registros por tarefa viram 720, mesma computação, 240× mais dados a persistir" é o tipo de argumento que uma banca de HPC aceita de imediato, porque isola a variável.

**Dois ambientes sustentam portabilidade.** AWS com FSx dedicado e SDumont com Lustre compartilhado, com o mesmo padrão qualitativo, é o que transforma "achamos um gargalo" em "o gargalo é da arquitetura, não da infraestrutura". É provavelmente a contribuição mais defensável do trabalho.

**As animações são argumentativas.** Revelar o MPI-IO depois de a plateia absorver a curva da implementação atual, e construir o fluxo de decisão em 5 cliques, usa animação para controlar a ordem do raciocínio — não para decorar.

**Assume o novo limite.** Dizer que o `MPI_File_open/close` passa a 11,6% em 32 nós mostra que você conhece o teto da própria solução. Bancas valorizam isso mais do que um resultado sem ressalva.

**As notas do apresentador são um ativo real.** A maioria dos slides tem mais de 1.000 caracteres, com números de reserva e respostas pré-formuladas para objeções previsíveis.

---

## 3. Lacunas, em ordem de risco

### RISCO ALTO

**3.1 O gancho de abertura nunca é respondido.**
O slide 2 pergunta "O SDDP ganharia escalabilidade?" e o deck termina em Trabalhos futuros. O laço fica aberto. Numa defesa isso é pior que não ter gancho: a plateia registra a pergunta e percebe que ela não voltou. **Ação:** um slide final espelhando o layout do slide 2, com a resposta na escala da pergunta — não com a arquitetura atual; paralelismo não falta (1,2 milhão de tarefas), a E/S impede.

**3.2 Não existe slide de trabalhos relacionados.**
A avaliação de banca de junho deu 0,0 ao Cap. 5 e apontou "onde estão os trabalhos relacionados?" como risco crítico nº 1. E-S paralela é uma área com literatura densa — ROMIO, *data sieving*, *two-phase I/O*, Liao *et al.*, PLFS, ADIOS, HDF5. Apresentar sem posicionar o trabalho nessa literatura é convite direto para a pergunta. **Ação:** um slide com 4–6 trabalhos e uma coluna de "o que este trabalho faz de diferente".

**3.3 Não existe slide de metodologia experimental.**
Em HPC, *como* se mediu é escrutinado tanto quanto o resultado. Hoje o setup está espalhado nas notas. Faltam num slide: hardware dos dois ambientes (r7i.12xlarge; nós do SDumont), rede, configuração do Lustre (`stripe_count=10`, `stripe_size=1 MB`, nº de OSTs), caso (1.536 cenários × 3 estágios mensais, 24 ranks/nó), 5 repetições com IC 95% e — o item que a avaliação de banca marcou como risco alto — **compilador, flags e configuração do `mpirun`**. **Ação:** um slide de setup antes do slide 10.

**3.4 A inconsistência do ponto de quebra do rendezvous continua aberta.**
Sua própria anotação registra que não era 64 KB nem 128 KB. Isso toca **três** slides: o 5 (Eager/Rendezvous), o 9 (limiar de 128 KB) e o 13 (tempo de bloqueio por tamanho). Se o número citado na fala divergir do texto, a banca puxa o fio. **Ação:** fixar o valor e alinhar os três.

### RISCO MÉDIO

**3.5 Falta o "por que MPI-IO independente e não outra coisa".**
O argumento existe — acesso contíguo, offsets calculáveis, coletiva custa sincronização — mas vive nas notas do slide 5. A pergunta "por que não HDF5 ou ADIOS?" estava mapeada como risco médio e não tem resposta visível. **Ação:** transformar em conteúdo de slide, ainda que como três linhas no slide 5.

**3.6 Só strong scaling, sem dizer que é uma escolha.**
Todos os experimentos fixam o caso e variam os nós. Nenhum slide nomeia isso. Uma banca de HPC pergunta por *weak scaling* quase por reflexo. **Ação:** nomear "estudo de strong scaling" no slide de metodologia e colocar weak scaling em trabalhos futuros.

**3.7 A ressalva de granularidade não está em nenhum slide.**
Em 32 nós há apenas 2 cenários por rank. Parte da perda de eficiência é granularidade, não E/S. Está nas notas, mas se um examinador levantar primeiro, a regressão de 16→32 vira "artefato do seu setup". **Ação:** uma linha no slide 12, assumindo você mesmo, com a defesa pronta — a fração de E/S é medida e instrumentada, não inferida por resíduo.

**3.8 A instrumentação é contribuição declarada e não tem slide.**
A contribuição nº 3 fala de "métricas operacionalmente equivalentes", e nada no deck mostra o que foi instrumentado nem como. Em HPC, metodologia de medição é contribuição legítima — sem slide, a afirmação fica sem lastro. **Ação:** integrar ao slide de metodologia.

**3.9 Não há placar quantitativo consolidado.**
As Conclusões citam números, mas não existe slide que mostre atual × MPI-IO lado a lado nos dois ambientes. O Cap. 4 tem as tabelas de resumo. **Ação:** um slide-tabela antes das Conclusões dá lastro visual ao fecho.

### RISCO BAIXO

**3.10 Assimetria AWS × SDumont.** O slide 17 (tempo de bloqueio, SDumont) está oculto, enquanto o equivalente da AWS (slide 13) está visível. Se o argumento é portabilidade, mostre os dois ou esconda os dois.

**3.11 Capa incompleta.** Orientador e banca ainda como `[preencher]`.

**3.12 Notas rasas em três slides.** Os slides 8 (163 caracteres), 13 (167) e 17 (43) estão muito abaixo do padrão do resto. O 13 é o mais preocupante, porque é resultado e é onde vive a questão do rendezvous.

**3.13 Sem slides de backup.** Uma defesa se ganha muitas vezes na arguição. Vale um bloco após o fim com: tabelas completas do Cap. 4, configuração detalhada, histograma de mensagens, e a rodada `ASYNC-FIX` do SDumont — que existe, tem resultado melhor em 32 nós (1.808 s contra 2.233 s) e **não** é a usada nas figuras. Se alguém perguntar, é melhor ter o slide do que improvisar.

---

## 4. Tempo

17 slides visíveis, mais 8 cliques de animação, dão cerca de **25 tempos de fala**. Para 30–40 minutos são 1,2 a 1,6 minuto por tempo. É viável, mas o risco clássico é gastar demais nos slides 2–9 e correr nos resultados. Se os slides recomendados entrarem (fechamento, relacionados, metodologia, placar), o deck vai a ~23 visíveis e fica **apertado para 30 minutos** — nesse caso, os candidatos a corte são os slides 13 e 17 (tempo de bloqueio), que podem ir para backup.

---

## 5. Prioridade sugerida

| # | Ação | Esforço | Impacto |
|---|---|---|---|
| 1 | Slide de fechamento respondendo o gancho | 15 min | Alto |
| 2 | Slide de trabalhos relacionados | 2–3 h | Alto |
| 3 | Slide de metodologia experimental e reprodutibilidade | 1 h | Alto |
| 4 | Fixar o ponto de quebra do rendezvous nos slides 5, 9 e 13 | 30 min | Alto |
| 5 | Slide-placar com o resumo quantitativo | 1 h | Médio |
| 6 | Ressalva de granularidade visível no slide 12 | 10 min | Médio |
| 7 | "Por que independente e não HDF5/ADIOS" no slide 5 | 20 min | Médio |
| 8 | Preencher orientador e banca na capa | 5 min | Médio |
| 9 | Bloco de backup para arguição | 1–2 h | Médio |
| 10 | Resolver a assimetria dos slides 13 e 17 | 5 min | Baixo |
