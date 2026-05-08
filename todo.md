## Correções pequenas

- Fazer experimentos assincronos independentes ( AWS e SDumont) - substituir figuras no texto.


- Introdução e capitulo 2.7 - Mario
- Capitulo 2
    - reduzir titulos da fundamentação teorica
    - MPI ( E MPI-IO ) sendo uma unica seção
    - falar sobre escrita independete e colletiva , vantagens de ambas
    - acesso continguo vs strides   
    - falar sobre bag-of-tasks 


- Trabalhar no capitulo III ( Começando amanhã as 21h)
    - Falar sobre as coisas do experimetos na proposta, Lustre , OSTs e MDTs     
    - Falar porque foi escolhido escrita independente e não coletiva, explicar da dificuldades de sincronizacao ( barrier ), repetições de blocos já enviados. ( sdesenho pipeline )
    - explicar da vantagem de não ter strides.
    - falar como a escrita assincrona pode ajudar na contenção
    
    - Eplica como cada processo vai acessar o OSTs.
    - mostrar os arquivos compartilhados
    - desenhar padrão dos dados
    - explicar como terá paralelizado a escrita dos resultados.
    - Trabalhos relacionados

- Conclusões e Trabalhos Futuros ( ROMIO )
- testes com placa de redes infinity band elastic Fabric

- ARTIGO
    - Modelo analitico
    - Validação com IOR
























- Com Trabalhos Relacionados + Conclusão + Cap. 3 expandido (espaço de design, hints MPI-IO, pseudocódigo). Defensável como mestrado adequado. Contribuição clara, metodologia razoável, posicionamento na literatura.
- Acima disso, com investigação dirigida da contenção de metadados no SDumont + variação sistemática de stripe + IOR como baseline + modelo analítico simples para o crossover. Dissertação forte com material para um artigo de conferência.



- ~~Figura de blocos de dados -  dificil de ler ( tirar espaço interno - aumentar espaço em cima) - label do eixo y errado. É a contenção do IOR.~~
- ~~Desvio padrão computação está errado no SDumont~~
- ~~Padronizacao das cores das figuras~~ 
- ~~Coordenação MPI-IO = MPI_File_Open/MPI_-File_Close.~~
- ~~Coletivas = MPI_File_Open/MPI_File_Close~~
- ~~cuidado com texo "mensagens"~~
- ~~melhorar figura histograma e texto~~ 
- ~~regenerar figuras e atualizar texto~~
- ~~Gerar novamente figura de quantidade de blocos de dados~~
- ~~Tirar label figura histrograma - faltou descrição dos eixos~~
- ~~corrigir labels figura blocos~~


##  Melhorias menores

- Figura sobre impacto E/S sobre o grupo de mensagem por tamanho
- Explicar formato resultados ( bloco e horarios)
- Impacto sobre 12 estagios ( AWS e SDumont )


# Relatório de Avaliação do Artigo

## Resumo

O Experimento AWS está numericamente consistente após as últimas atualizações. As tabelas, os gráficos de banda e tempo, e o texto explicativo agora seguem a mesma interpretação dos dados.

Ainda existem pendências importantes fora da seção AWS, principalmente na introdução, na fundamentação, na bibliografia e no Experimento SDumont.

## Pontos Críticos

### 1. Placeholders no Documento

Ainda há campos não finalizados:

- Orientador e examinadores estão genéricos.
- Dedicação ainda está como `[a definir]`.
- Agradecimentos ainda contêm `ToDp`.

Também há marcações `ToDp` e `ToDO` no corpo do texto, especialmente na introdução e na seção sobre SDDP.

### 2. Bibliografia Incompleta

O arquivo `bibliografy.bib` ainda possui várias entradas com `TODO`.

As citações mais críticas são:

- `refNeeed`
- `mpiCite`

Essas entradas aparecem no texto e precisam ser substituídas por referências reais.

### 3. Experimento SDumont Desalinhado

O texto do Experimento SDumont não bate com os valores das tabelas.

Exemplo da implementação atual:

- Texto cita valores como `8.444 s`, `5.921 s` e `7.805 s`.
- Tabela mostra `9.376,80 s`, `6.841,99 s`, `6.981,25 s` e `9.082,37 s`.

Exemplo da implementação MPI-IO:

- Texto cita `9.375 s`, `5.580 s`, `5.366 s` e `6.407 s`.
- Tabela mostra `10.343,93 s`, `6.430,57 s`, `6.342,98 s` e `7.592,64 s`.

Essa seção precisa ser revisada com base nos CSVs/tabelas atuais.

## Figuras e Texto

### Experimento AWS

Situação atual: consistente.

- `Banda_AWS.png` bate com as tabelas.
- `Tempo_execucao_AWS.png` bate com as tabelas.
- O texto agora explica corretamente que:

```text
Total = Avg_Simulation + Avg_comunication_per_process




