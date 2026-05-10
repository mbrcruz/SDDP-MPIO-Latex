---
arquivo: chapters/04_avaliacoes.tex (892 linhas)
data da avaliação: 2026-05-09 (versão pós-reordenação AWS→SDumont, novos números do SDumont, Síntese das avaliações)
---

# Avaliação do Capítulo 4 — Avaliações

## Nível geral

**4,5 / 5 — Adequado para mestrado, próximo do excelente.**

O capítulo entrega um arco narrativo coerente: introdução com setup
e histograma de blocos → AWS (ambiente isolado, atual / MPI-IO /
comparativa / OSTs) → SDumont (ambiente compartilhado, atual / MPI-IO /
comparativa) → Síntese consolidando os dois ambientes. O resultado
estruturalmente mais forte do capítulo --- o contraste qualitativo
entre o perfil monotonicamente crescente da MPI-IO e o perfil errático
ou degradado da implementação atual --- aparece nas duas plataformas e
está bem articulado na Síntese. As tabelas estão consistentes com as
figuras (verifiquei contra o `plot.csv` atualizado), e o tratamento do
custo da Coordenação MPI-IO agora distingue corretamente o "fixo em
relação à carga útil" do "variável com o número de nós".

Os ajustes a fazer são quase todos de reprodutibilidade,
harmonização entre as duas seções e elementos pontuais de
contextualização --- nada estrutural.

---

## 1. Pontos fortes

1. **Recorte experimental coerente.** Mesmo dataset (PMO/PAR
   out/2023, 1.536 cenários, 3 estágios mensais), mesmo regime
   (\textit{strong scaling}), mesmo mapeamento (1 \textit{rank} por
   núcleo físico) nos dois ambientes. Permite comparação direta.

2. **Decomposição por classe de tamanho.** A análise dos quatro
   painéis em `EnvioPorTamanho_AWS` e `EnvioPorTamanho_SDumont` é o
   ponto técnico mais sofisticado: revela onde cada arquitetura ganha
   e perde, e permite o argumento qualitativo de "ponto de troca em
   função da escala".

3. **Ablação de OSTs no AWS.** Isolar o efeito da camada de
   armazenamento (4 vs. 10 OSTs em 16 e 32 nós) é um movimento
   metodológico forte. O dado mais expressivo --- 143 Gb/s vs.\
   36,7 Gb/s em 32 nós ao quadruplicar OSTs --- sustenta diretamente o
   argumento da Síntese sobre dimensionamento como parâmetro de projeto.

4. **Variabilidade reportada.** Todas as tabelas trazem desvio padrão
   ($\pm$). Para Total, o desvio é a soma quadrática implícita de
   simulação e comunicação. Boa prática para mestrado.

5. **Honestidade com limitações.** O texto reconhece (a) o sobrecusto
   da MPI-IO em 2 e 4 nós, (b) a inflação relativa da Coordenação MPI-IO
   por causa do tamanho reduzido das execuções, (c) o caráter
   compartilhado do Lustre do SDumont como fator de variabilidade.
   Termina sem sobrevender o resultado.

6. **Síntese das avaliações.** Faz a amarração que faltava entre AWS
   e SDumont, distingue "estrutural" (contraste qualitativo) de
   "magnitude" (depende do ambiente), e fecha apontando para o
   Capítulo 5.

---

## 2. Pontos a melhorar

### 2.1 Reprodutibilidade — alta prioridade

Sem essas informações, ninguém consegue replicar os experimentos.

7. **Número de repetições por configuração.** As tabelas trazem
   desvio padrão, mas o capítulo não diz quantas execuções foram
   feitas por ponto. Sugestão: incluir uma frase na introdução do
   capítulo do tipo *"cada configuração foi executada $N$ vezes; os
   valores reportados correspondem à média e ao desvio padrão dessas
   $N$ amostras"*. Sem $N$, o desvio fica incompleto.

8. **Versão de compilador e \textit{flags}.** A introdução de cada
   seção menciona MPICH2 3.2, mas não menciona compilador (Intel
   ifort? GCC? versão?), flags de otimização, nem a versão do
   próprio SDDP utilizada. Para mestrado em sistemas distribuídos é
   esperada essa informação.

9. **Stripe count do Lustre.** Está dito que `stripes` são de 1 MB
   nos dois ambientes, mas falta dizer com quantos OSTs cada arquivo
   é \textit{striped} por padrão (`lfs setstripe -c`). Esse parâmetro
   afeta diretamente os resultados.

10. **`Hardware` lado a lado.** Hoje as descrições de AWS (l. 70–89) e
    SDumont (l. 470–488) estão em prosa, dificultando a comparação
    direta. Sugiro acrescentar uma pequena tabela na introdução do
    capítulo, lado a lado, com: CPU, núcleos físicos, memória, rede,
    sistema de arquivos, OSTs, MDTs, \textit{stripe size}. Um leitor
    consegue ler todas as diferenças relevantes em 30 segundos.

### 2.2 Harmonização AWS ↔ SDumont — média prioridade

11. **Faixa de escalas diferente.** AWS chega a 32 nós; SDumont para em
    16. O leitor pode interpretar isso como omissão. Acrescentar uma
    frase, na introdução do SDumont ou na Síntese, explicando \textit{por
    que} 32 nós não foi rodado no SDumont (cota do projeto LNCC?
    indisponibilidade do recurso? variabilidade do compartilhamento
    desestabilizou a medição?).

12. **Subseção OSTs só existe na AWS.** A topologia do Lustre do
    SDumont é fixa (6 OSTs, 1 por OSS). Sugiro acrescentar uma frase
    no início da subseção 4.1.4, do tipo: *"Esta análise foi
    conduzida exclusivamente no Experimento AWS porque o Lustre do
    SDumont possui topologia fixa de 6~OSTs (um por OSS), sem
    possibilidade de variação operacional."* Isso elimina a
    impressão de assimetria.

13. **Banda absoluta em 2 nós: AWS vs.\ SDumont.** A banda da
    implementação atual é parecida em 2 nós entre os dois ambientes
    (60,5 vs.\ 62,8 Gb/s), apesar do hardware de rede ser muito
    diferente (Ethernet 18,75 Gb/s na AWS, InfiniBand EDR 100 Gb/s
    no SDumont). Isso ocorre provavelmente porque "banda" mede o
    \textit{layer} de comunicação \texttt{MPI\_Send}, não o egresso
    do nó pelo NIC --- e parte da banda agregada vem de cópias
    intra-nó (o escritor está no mesmo nó que parte dos emissores,
    em pequena escala). Vale uma nota explicando o que exatamente
    está sendo medido em "Banda agregada", para que o leitor não
    interprete como banda de saída do NIC.

14. **MPI-IO em 2 nós: SDumont 5,5 Gb/s vs.\ AWS 33,8 Gb/s.** A
    diferença é de 6×. Não há discussão no texto sobre por que a
    MPI-IO em pequena escala é tão mais lenta no SDumont. Hipóteses
    possíveis: custo fixo do ClusterStor; latência de metadados no
    MDS único; \textit{stripe count} default diferente; concorrência
    com outras cargas. Acrescentar pelo menos uma frase com a
    hipótese mais provável evitaria a sensação de número órfão.

### 2.3 Detalhes editoriais — baixa prioridade

15. **`Caption` da Figura `Tempo_execucao_AWS` é genérico.** Está como
    "Tempo de execução no Experimento AWS." (l. 362). A figura
    análoga do SDumont (l. 752) já foi atualizada para
    "Decomposição do tempo médio por processo das implementações
    atual e MPI-IO no Experimento SDumont." Convém harmonizar:
    *"Decomposição do tempo médio por processo das implementações
    atual e MPI-IO no Experimento AWS, separando computação,
    comunicação, E/S e Coordenação MPI-IO."*

16. **Histograma de blocos sem origem explícita.** A
    Figura~\ref{fig:histograma_mensagens} (l. 58–64) traz números
    absolutos (1.801.728 blocos etc.) mas o texto diz apenas "ao longo
    do experimento". De qual experimento? AWS? SDumont? Configuração
    específica? Sugiro especificar (ex.: *"agregado da execução com
    16~nós no Experimento AWS, implementação atual"*).

17. **Repetição entre conclusão da seção SDumont (l. 811–831) e a
    Síntese das avaliações (l. 837–891).** Os parágrafos finais da
    seção SDumont já dizem boa parte do que a Síntese retoma sobre o
    SDumont. Pode-se enxugar a conclusão da seção SDumont para um
    parágrafo curto (apenas o diagnóstico local), deixando a
    contextualização cross-ambientes para a Síntese.

18. **`Speedup` ideal nas figuras.** Em nenhuma das figuras de banda
    ou de tempo aparece a linha de \textit{speedup} ideal (banda
    proporcional a $N$, ou tempo $\propto 1/N$). Para um mestrado
    em sistemas distribuídos, esse \textit{baseline} visual é
    convencional --- ajuda a quantificar visualmente o quanto a
    realidade se afasta do ideal. Considerar adicionar.

19. **Termo "\textit{layer} de escrita".** Aparece l. 568 ("banda
    agregada do \textit{layer} de escrita"). É anglicismo
    desnecessário; em português técnico usa-se "camada de
    escrita".

20. **Citação solta a `\cite{intel:23,aws:24}`** (l. 89). Verificar
    que essas chaves resolvem na bibliografia (não tive acesso para
    confirmar agora). Idem `\cite{Amdahl:67}` (l. 31) e
    `\cite{Rwe:99,Phrrbrw:09}` (l. 11, 53).

---

## 3. Verificações de nível de mestrado

- **Rigor acadêmico:** adequado. Hipóteses (gargalo do escritor único,
  saturação por concorrência, sobrecusto fixo da MPI-IO) são todas
  testáveis e testadas. Falta apenas o número de repetições e detalhes
  de compilação para reprodutibilidade plena.
- **Análise de resultados:** muito boa. Os números são interpretados
  causalmente, não apenas descritos. O argumento qualitativo
  ("monotônico vs.\ errático") é mais forte do que apenas comparar
  picos.
- **Contribuição:** clara — a arquitetura proposta endereça o gargalo
  estrutural identificado no Cap. 2, com ganhos demonstrados nos dois
  ambientes.
- **Limitações:** declaradas explicitamente na Síntese (faixa
  testada, custo de coordenação inflado, restrição à fase de simulação
  final).
- **\textit{Strong scaling} formalmente caracterizado:** sim
  (l. 28–41). Mas falta o \textit{baseline} ideal nas figuras (item 18).

---

## 4. Lista priorizada de ações

**Alta prioridade (pré-defesa):**

1. Acrescentar número de repetições por configuração (item 7).
2. Adicionar versão do compilador, \textit{flags} e versão do SDDP
   (item 8).
3. Documentar \textit{stripe count} do Lustre nos dois ambientes
   (item 9).
4. Justificar a faixa de escalas diferente entre AWS (até 32) e
   SDumont (até 16) (item 11).
5. Acrescentar nota dizendo que a análise de OSTs só foi feita no AWS
   por restrição da topologia do SDumont (item 12).

**Média prioridade:**

6. Tabela de hardware lado a lado AWS vs.\ SDumont na introdução do
   capítulo (item 10).
7. Esclarecer o que "Banda agregada" mede (\texttt{MPI\_Send}
   vs.\ NIC vs.\ Lustre), idealmente uma frase na introdução
   (item 13).
8. Acrescentar frase explicando o sobrecusto da MPI-IO em 2 nós no
   SDumont (item 14).
9. Harmonizar caption da Figura `Tempo_execucao_AWS` com a do
   SDumont (item 15).
10. Especificar a origem dos dados do histograma da introdução
    (item 16).
11. Reduzir redundância entre a conclusão da seção SDumont e a
    Síntese (item 17).

**Baixa prioridade (polimento):**

12. Adicionar curva de \textit{speedup} ideal às figuras de banda /
    tempo (item 18).
13. Trocar "\textit{layer} de escrita" por "camada de escrita"
    (item 19).
14. Verificar resolução das chaves de citação (item 20).
