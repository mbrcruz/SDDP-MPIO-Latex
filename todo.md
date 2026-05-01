## Correções pequenas



- ~~Tirar label figura histrograma - faltou descrição dos eixos~~

- ~~corrigir labels figura blocos~~

-- Figura de blocos de menagens dificil de ler ( tirar espaço interno - aumentar espaço em cima)

- Rodar 4 OSts com 1536 - regenerar figuras


##  Melhorias 

-- impacto E/S sobre o grupo de mensagem por tamanho


## Plano de Melhorias gerais

## 1. Corrigir coerência numérica

- Atualizar todos os valores citados no texto usando as tabelas atuais como fonte principal.
- Corrigir os valores do Experimento SDumont.
- Corrigir os valores do Experimento AWS.
- Recalcular percentuais, speedups e razões de ganho.
- Garantir que texto, tabelas e figuras apresentem os mesmos números.

## 2. Resolver pendências no texto

- Remover ou substituir todas as marcações `ToDp` e `ToDO`.
- Completar os agradecimentos.
- Expandir a introdução onde há indicação pendente.
- Finalizar a descrição da organização da dissertação.
- Detalhar melhor o SDDP e sua relação com o problema estudado.

## 3. Ajustar o Experimento SDumont

- Corrigir a afirmação de que foram usados até 32 nós.
- Manter apenas os resultados de 2, 4, 8 e 16 nós.
- Reescrever a análise de tempo total com os valores corretos.
- Reescrever a análise da versão MPI-IO com os valores corretos.
- Evitar comparações com AWS antes de o Experimento AWS ser apresentado.

## 4. Ajustar o Experimento AWS

- Reescrever a análise de largura de banda com os valores atualizados.
- Corrigir a razão de ganho da MPI-IO sobre a implementação atual.
- Reescrever a análise de tempo total.
- Corrigir a redução percentual em 32 nós.
- Verificar se todas as conclusões seguem diretamente dos dados das tabelas.

## 5. Definir claramente as métricas

- Explicar o significado de:
  - tempo de simulação;
  - tempo de E/S;
  - tempo de comunicação;
  - tempo de operações coletivas;
  - tempo total;
  - largura de banda agregada;
  - percentual de E/S;
  - speedup.
- Indicar se o símbolo `±` representa desvio padrão, intervalo de confiança ou outra medida.
- Garantir que as fórmulas usadas nas tabelas sejam descritas no texto.

## 6. Melhorar as figuras

- Regenerar `Experimento_OSTs.png`.
- Regenerar `Experimento_OSTs_banda.png`.
- Regenerar `histograma_mensagens.png`.
- Usar o mesmo estilo visual das figuras novas.
- Revisar as figuras de tempo para reduzir excesso de informação.
- Separar, se necessário, os gráficos de tempo em painéis por implementação.
- Alinhar o texto das seções com o conteúdo real das figuras.

## 7. Revisar figuras de mensagens por tamanho

- Verificar se as figuras usam classes agregadas ou tamanhos reais de mensagem.
- Se usarem classes agregadas, reescrever o texto para falar em mensagens pequenas, médias, grandes e muito grandes.
- Se o texto mantiver valores como `50 MB` e `100 MB`, regenerar as figuras com esses tamanhos explícitos.

## 8. Melhorar as tabelas

- Reduzir casas decimais para melhorar legibilidade.
- Alinhar colunas numéricas.
- Considerar o uso de `siunitx`.
- Separar tabelas muito largas, se necessário.
- Padronizar nomes de colunas entre SDumont e AWS.
- Garantir que as legendas expliquem o conteúdo sem ambiguidade.

## 9. Revisar a subseção de OSTs

- Deixar claro que a avaliação de OSTs pertence ao Experimento AWS.
- Explicar a configuração com 10 OSTs e 6 OSTs.
- Remover possíveis contradições entre impacto no tempo total e impacto na largura de banda.
- Adicionar tabela com os valores usados nas figuras, se possível.

## 10. Corrigir referências bibliográficas

- Substituir todas as entradas `TODO` da bibliografia por referências reais.
- Conferir se todas as citações no texto têm entrada bibliográfica válida.
- Remover referências não usadas.
- Padronizar formato dos autores, títulos, conferências, anos e URLs.

## 11. Criar uma síntese final dos experimentos

- Adicionar uma seção curta após o Experimento AWS.
- Comparar SDumont e AWS somente depois que ambos forem apresentados.
- Destacar resultados comuns entre os ambientes.
- Separar claramente efeitos de:
  - arquitetura de E/S;
  - sistema de arquivos;
  - contenção de metadados;
  - número de OSTs;
  - escala de execução.

## 13. Revisar conclusão

- Remover redundâncias como “arquitetura de E/S MPI-IO, baseada em MPI-IO”.
- Garantir que a conclusão não afirme ganhos não demonstrados pelos dados.
- Diferenciar conclusões específicas do SDumont, específicas do AWS e conclusões gerais.
- Incluir limitações do estudo, especialmente sobre escala, número de OSTs e ausência dos resultados de 32 nós no SDumont