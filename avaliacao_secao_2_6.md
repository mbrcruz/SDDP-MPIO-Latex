---
arquivo: chapters/02_fundamentacao.tex (linhas 329 a 569)
seção avaliada: 2.6 — Algoritmo SDDP (incluindo 2.6.1 e 2.6.2)
data da avaliação: 2026-05-08
---

# Avaliação da Seção 2.6 — Algoritmo SDDP

## Nível geral

**4 / 5 — Adequado para mestrado, com ajustes pontuais recomendados.**

A seção tem um arco argumentativo bem encadeado: define o SDDP, isola
explicitamente a fase de simulação final como objeto de estudo, demonstra que
ela é *bag-of-tasks*, mostra como a granularidade horária amplia o volume de
saída, descreve o formato dos dados e, por fim, caracteriza a arquitetura
atual de E/S como o gargalo a ser atacado. Esse encadeamento "problema →
independência → bag-of-tasks → gargalo deslocado para E/S → arquitetura
atual" é exatamente o que o capítulo precisa entregar para preparar a
proposta no Capítulo 3. Os pontos a melhorar são quase todos de quantificação,
uniformização terminológica e enxugamento de repetições — não há problema
estrutural.

---

## 1. Corpo principal da Seção 2.6 (linhas 329 a 397)

### Pontos fortes

- **Recorte explícito do escopo.** "Esta dissertação concentra-se exclusivamente
  na fase de simulação final" (l. 346–347) é um recorte metodológico forte e
  cumpre o critério de "problema claramente delimitado".
- **Conexão causal bem-feita.** A frase "É também o que desloca o gargalo da
  computação para a persistência dos resultados, à medida que o número de
  cenários cresce" (l. 360–362) entrega em uma sentença a justificativa
  central da dissertação inteira.
- **Justificativa do regime horário.** O argumento de que a inserção de FER
  exige resolução horária (l. 374–377) é correto e relevante, e amarra a
  motivação do trabalho à transição em curso no setor elétrico.
- **Citações bibliográficas adequadas.** `MvLm:91` resolve corretamente para
  Pereira & Pinto (1991, *Mathematical Programming*) — verifiquei na
  `bibliografy.bib` e no `.bbl`. `Cirne:2003` (Grid Computing for Bag of
  Tasks) é a referência canônica e está bem aplicada.

### Pontos a melhorar

1. **"Ordem de magnitude" subestima o salto.** O texto diz que o caso horário
   gera "ordem de magnitude maior que o caso tradicional por blocos"
   (l. 379–380). A razão real é 720 horas / 5 patamares = 144×, ou seja,
   ~2,16 ordens de magnitude. Recomendo trocar por **"duas ordens de
   magnitude maior"** ou simplesmente **"da ordem de 100× a 150× maior"**.

2. **Particionamento de cenários sem balanceamento.** A frase "os cenários são
   particionados entre os \textit{ranks} MPI e resolvidos em paralelo, de modo
   que o tempo total da fase de simulação fica limitado pelo cenário mais lento"
   (l. 356–359) pressupõe distribuição estática. Vale uma frase explicitando
   se o particionamento é estático (round-robin / blocos) ou dinâmico
   (master–worker), porque isso afeta diretamente a interpretação dos resultados
   do Capítulo 4. Sugestão: *"Na implementação atual, os cenários são
   distribuídos estaticamente entre os ranks no início da execução."*

3. **Repetição de "fase de simulação final".** A expressão aparece 6 vezes
   nos parágrafos das l. 338–362. A partir do segundo parágrafo, basta
   "essa fase" ou "a simulação final".

4. **Falta uma menção mínima ao subproblema de estágio.** Mesmo que o foco
   seja Sistemas Distribuídos e não Otimização, a dissertação precisa que o
   leitor entenda *o que* cada célula da Figura 2.3 representa em termos de
   carga computacional e volume de saída por subproblema. Uma equação de
   Bellman simplificada (ou pelo menos uma frase do tipo *"cada subproblema
   resolve um problema linear de despacho determinístico para um par
   (estágio, cenário) sob a política convergida"*) seria suficiente. Sem isso,
   o leitor não-especialista em SDDP não consegue julgar se a aplicação é
   *compute-bound* ou *I/O-bound* nos casos avaliados.

5. **Quantificar o volume agregado por iteração.** A última frase do parágrafo
   (l. 382–386) afirma que o volume cresce linearmente com cenários × estágios
   × granularidade. Isso já fica concreto na Subseção 2.6.1, mas seria muito
   mais forte se aqui já aparecesse o **número que de fato será atacado pelo
   experimento**: 1.536 cenários × 3 estágios × 720 horas × ~300 agentes ×
   4 bytes ≈ 4 GB por iteração. Esse é o "elefante na sala" e merece estar
   visível antes mesmo da subseção 2.6.1.

### Avaliação da Figura 2.3 — `SDDP_cenarios_estagios.png`

Inspecionei a imagem.

- **Pontos fortes:** matriz 3 × 1.536 com cores distintas por estágio,
  anotação "Cenários independentes entre si" e seta indicando paralelismo
  entre cenários. A figura é direta, autoexplicativa e está alinhada com o
  *setup* experimental (1.536 cenários, 3 estágios), o que reforça
  consistência com o Capítulo 4.
- **Sugestões:**
  - O caption (l. 391–396) diz que cenários "podem ser distribuídos entre
    ranks MPI". Acrescentar a palavra **estaticamente** se for o caso, para
    casar com a sugestão (2) acima.
  - Considerar adicionar, dentro de uma das células, a anotação do que
    o subproblema produz (ex.: *"720 linhas × N agentes"*), antecipando a
    Figura 2.7.
  - A figura é PNG. Como as outras figuras "didáticas" da seção 2.1 são em
    TikZ (vetoriais), há uma quebra de estilo. Não é problema funcional, mas
    se possível, regerar em TikZ ou exportar em SVG/PDF para preservar
    qualidade no documento final.

---

## 2. Subseção 2.6.1 — Padrão dos dados de saída (linhas 399 a 530)

### Pontos fortes

- **Cálculos numéricos explícitos.** Os volumes 11.520 B (1 agente) e
  872.640 B (300 agentes) por par (estágio, cenário) tornam o argumento
  concreto e quantitativo — exatamente o que o avaliador procura em uma
  fundamentação de mestrado.
- **Dois formatos contrastados.** Mostrar primeiro o formato por patamares
  (Figura 2.4) e depois o horário (Figura 2.5) deixa claro por que o trabalho
  só é interessante no segundo regime.
- **Conexão clara com a motivação.** O parágrafo da l. 444–452 amarra a
  necessidade de resolução horária à variabilidade intradiária de FER,
  reforçando a coerência com o Capítulo 1.

### Pontos a melhorar

1. **"Agentes" não está definido.** Os termos $A_1, \ldots, A_N$ aparecem nas
   figuras e no texto sem definição. Vale uma frase explicando, por exemplo:
   *"Cada coluna $A_i$ corresponde a um agente do sistema — usina hidrelétrica,
   térmica, parque eólico/solar ou linha de transmissão monitorada — cujos
   resultados (geração, déficit, intercâmbio etc.) são registrados por hora."*

2. **Origem do "300 agentes".** O número aparece sem motivação (l. 461–463).
   Sugestão: *"Em uma instância típica do PMO/PAR, cada estágio
   pode envolver da ordem de 300 agentes monitorados (usinas hidrelétricas,
   térmicas e parques renováveis), o que motiva avaliar empiricamente esse
   regime."*

3. **Premissa de 4 bytes/valor não justificada.** O cálculo "considerando
   valores de 4 bytes" (l. 460) implica precisão simples (float). O SDDP
   tradicionalmente trabalha em precisão dupla por causa do condicionamento
   do problema dual e dos custos econômicos. Recomenda-se uma nota explicando
   se o **arquivo de saída** de fato usa float (provavelmente sim, por
   tamanho) mesmo que o **núcleo de cálculo** use double — ou ajustar o
   cálculo para 8 bytes se for o caso.

4. **Redundância de colunas (estágio, cenário).** Nos cálculos, as colunas de
   identificador (estágio, cenário, hora) entram no total: "4 colunas: estágio,
   cenário, hora e $A_1$". Em formatos binários compactos, esses identificadores
   costumam ser metadados de cabeçalho ou implícitos pelo *offset*, e não
   replicados em cada linha. Uma frase do tipo *"a representação aqui
   adotada inclui as colunas-chave em cada linha por compatibilidade com o
   arquivo CSV de saída atual; em uma representação binária essas colunas
   poderiam ser implícitas"* eliminaria a ambiguidade — e ainda joga lenha
   para o argumento do Capítulo 3, em que o *offset* MPI-IO permite remover
   essa redundância.

5. **Notação inconsistente com o Capítulo 3.** A 2.6.1 usa
   $(\text{estágio}, \text{cenário}, \text{hora})$ na forma textual e
   $v_{1,1,h,i}$ nas figuras. O Capítulo 3 usa a tupla compacta $(e, c, h)$
   e o tamanho de registro $S_r$. Uniformizar a notação já em 2.6.1 facilita
   a leitura: trocar "estágio, cenário, hora" por **"$(e, c, h)$"** em ao
   menos uma das aparições.

6. **Patamar não foi definido.** A subseção introduz "patamar de carga"
   (l. 405–410) sem defini-lo. A 2.5 toca rapidamente no PMO mas não
   explica patamar. Uma frase: *"patamar é um intervalo agregado dentro do
   estágio que representa um nível típico de carga (pesado, médio, leve)"*
   resolve.

### Avaliação das Figuras 2.4 e 2.5 (TikZ)

- **Pontos fortes:** As duas tabelas-figura ilustram bem a estrutura
  hierárquica dos dados; o uso de cores (verde para chaves, laranja/azul para
  valores) facilita a leitura.
- **Sugestões:**
  - Em 2.4 (patamares), o caption diz "cinco patamares" — verifique se este
    é o número padrão; o ONS hoje usa três patamares (pesado, médio, leve) e
    em alguns estudos cinco. Confirmar e citar.
  - Em 2.5, a coluna "$\cdots$" no meio sugere variáveis intermediárias mas
    o leitor pode ler como "horas omitidas". Considere posicionar os "$\cdots$"
    apenas em linhas (omitindo linhas) e listar agentes $A_1, A_2, A_3, A_N$
    sem reticências entre colunas — ou reforçar no caption que as reticências
    são por agentes.

---

## 3. Subseção 2.6.2 — Arquitetura atual de E/S (linhas 532 a 569)

### Pontos fortes

- **Identificação precisa do gargalo.** A separação "rank 1 escritor / rank 0
  controlador" no mesmo nó mestre, compartilhando o mesmo adaptador de rede,
  é exatamente a hipótese que o Capítulo 4 confirma empiricamente.
- **Lista explícita de hipóteses.** Apresentar as três hipóteses (adaptador
  do mestre, fluxo sequencial recv+write, propagação do atraso aos demais
  ranks) ajuda o leitor a estruturar o que será testado.

### Pontos a melhorar

1. **Caption da Figura 2.6 é fraco demais.** O `.tex` registra o caption como
   *"Algoritmo SDDP com processo escritor."* (l. 547). Inspecionei a imagem:
   ela é detalhada — mostra rank 0 e rank 1 no nó mestre, ranks 2..N nos nós
   de computação, fluxo `MPI_Send(buffer)` e o sistema de arquivos. Um caption
   à altura seria: *"Arquitetura atual de E/S do SDDP: ranks 2..N enviam
   blocos via `MPI_Send` ao rank escritor (rank 1), que compartilha o
   adaptador de rede do nó mestre com o rank 0 (controle) e serializa as
   gravações no sistema de arquivos."*

2. **Inconsistência entre as hipóteses da 2.6.2 e da abertura do Cap. 3.**
   A 2.6.2 lista **três** hipóteses; a abertura do Capítulo 3 (l. 21–27) fala
   em **dois** gargalos (comunicação centralizada e armazenamento serializado).
   Não são incompatíveis (a hipótese 3 da 2.6.2, sobre propagação do atraso,
   é uma consequência das outras duas), mas a leitura sequencial fica
   incoerente. Recomendo: ou condensar 2.6.2 em duas hipóteses casadas com
   o Cap. 3, ou abrir o Cap. 3 lembrando explicitamente as três hipóteses
   da 2.6.2 e mostrando como a proposta endereça cada uma.

3. **Hipóteses sem critério de teste.** Cada hipótese deveria fechar com uma
   frase do tipo *"esta hipótese é avaliada na Seção 4.X por meio da métrica
   Y"*. Sem isso, ficam especulativas. Especificamente:
   - Hipótese (i) adaptador → testada por **bandwidth efetiva no rank
     escritor vs. agregada** (Seção 4 do experimento).
   - Hipótese (ii) fluxo sequencial → testada por **tempo de bloqueio e
     overlap recv+write**.
   - Hipótese (iii) atraso induzido → testada por **tempo de espera dos
     ranks produtores nas chamadas `MPI_Send`**.

4. **Faltam números.** A 2.6.2 fala em "alto volume de dados" sem
   quantificar. Conectando com 2.6.1: 1.536 cenários × 3 estágios ×
   872.640 B ≈ **4 GB que precisam atravessar um único `MPI_Recv` e uma
   única gravação serial por iteração**. Esse número, dito aqui, fecha o
   argumento da seção inteira.

5. **Verificar a separação rank 0 vs. rank 1.** A imagem confirma que a
   arquitetura atual realmente separa "rank 0 = gerência" e "rank 1 = escritor"
   no nó mestre. Boa prática: citar a função/módulo do código onde essa
   atribuição é feita (ex.: *"essa separação está implementada em
   `module_X` do código-fonte do SDDP"*). Isso dá reprodutibilidade e
   ancora a fundamentação teórica no artefato real avaliado.

6. **Termos: "buffer de dados".** O texto repete "*buffer* de dados" 6 vezes
   em 30 linhas (l. 537–569). Substituir alguns por "bloco" ou "lote" sem
   prejuízo de sentido.

---

## 4. Consistência cruzada

| Item | Cap. 1 | Cap. 2.6 | Cap. 3 | Cap. 4 |
|---|---|---|---|---|
| Foco em simulação final | implícito | explícito (l. 346) | implícito | explícito (l. 13–17) |
| Bag-of-tasks | ausente | central (l. 353) | implícito | implícito |
| 1.536 cenários × 3 estágios | ausente | implícito (Fig. 2.3) | ausente | explícito (l. 14–16) |
| Número de "agentes" | ausente | 300 mencionado | ausente | ausente |
| Modelo atual = rank único escritor | ausente | claro (2.6.2) | claro (l. 4–8) | implícito |
| Hipóteses do gargalo | ausentes | três (2.6.2) | duas (Cap. 3) | testadas como métricas | 

**Recomendação:** uniformizar (a) o número de hipóteses entre 2.6.2 e Cap. 3
e (b) o vocabulário de "agentes" — ou retira-se da 2.6.1 e reaparece no
Cap. 4 com o número exato do experimento, ou mantém-se em 2.6.1 com a
motivação concreta sugerida no item 2 da subseção 2.6.1.

---

## 5. Lista priorizada de ações

**Alto impacto (corrigir antes da próxima leitura do orientador):**

1. Corrigir caption da Figura 2.6 — o atual é genérico demais para uma figura
   tão informativa.
2. Uniformizar a contagem de hipóteses entre a 2.6.2 (três) e a abertura do
   Cap. 3 (duas).
3. Trocar "ordem de magnitude" por "duas ordens de magnitude" (ou ~144×) na
   l. 379–380.
4. Quantificar o volume agregado por iteração (≈ 4 GB) explicitamente, seja
   ao final do corpo principal da 2.6, seja na 2.6.2.

**Médio impacto:**

5. Definir "agentes" e justificar o "300" na 2.6.1.
6. Definir "patamar" antes da Figura 2.4.
7. Justificar (ou ajustar) a premissa de 4 bytes por valor.
8. Para cada hipótese da 2.6.2, anexar a métrica/seção do Cap. 4 que a testa.
9. Esclarecer se o particionamento de cenários é estático ou dinâmico.

**Baixo impacto (polimento):**

10. Reduzir repetições de "fase de simulação final" e "buffer de dados".
11. Padronizar notação $(e, c, h)$ entre 2.6.1 e Cap. 3.
12. Considerar regerar `SDDP_cenarios_estagios.png` em TikZ para manter
    coerência visual com as outras figuras didáticas.

---

## 6. Verificações de nível de mestrado

- **Rigor acadêmico:** adequado. Recorte do problema explícito; hipóteses
  enumeradas. Falta apenas amarrar cada hipótese a um teste empírico.
- **Revisão bibliográfica:** referências corretas e bem aplicadas, embora a
  bibliografia do SDDP seja minimalista (apenas Pereira & Pinto 1991). Para
  uma fundamentação completa, considerar incluir uma referência mais recente
  sobre paralelização do SDDP em HPC (ex.: trabalhos do CEPEL/PSR sobre
  Newave ou trabalhos sobre `SDDP.jl`).
- **Contribuição original:** a Seção 2.6 é fundamentação, não contribuição —
  e cumpre esse papel adequadamente.
- **Análise de resultados:** N/A para este capítulo (é fundamentação).
- **Reprodutibilidade:** a 2.6.2 ganharia com um *pointer* para o módulo de
  código onde a arquitetura atual está implementada.
