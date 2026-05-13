## Correções pequenas

- Fazer experimentos assincronos independentes ( AWS e SDumont) - substituir figuras no texto.


- Trabalhar no capitulo III ( Começando amanhã as 21h)
    - ~~Introdução da arquitetura proposta~~
    - ~~Visão geral e explicação da arquitetura proposta.~~
    - ~~novo pipeline SDDP - execução ,  escrita , reeexução , reescrita de dados e independencia de processos. ~~  
    - ~~Relacionar com arquivos compartilhados - blocos de dados separados em OSTs~~
    - ~~Apresentar o modelo de Escrita independente E/S , e dizer porque não foi selecionado a escrita coletiva que precisa de um certa coordenação entre os processos, pois o SDDP funciona resolver problemas indepentes e sincronizacao de escrita pode ser prejudicial neste casp.~~
    - ~~Mostrar como os arquivos são distribuidos em stripes.~~      
    - Formato dados
    - Falar como que foi implementado com escrita assincrona para blocos até 128K e sincrona para blocos maiores  ( Mencionar Eager e Rendevous ) - minimzar pressão pelo uso de memoria.
    - Processo Gerenciador de tarefas";
    






- Introdução e capitulo 2.7 - Mario
- Capitulo 2
    - ~~reduzir titulos da fundamentação teorica~~
    - Bag-of-tasks
    - MPI (  MPI-IO ) sendo uma unica seção - Melhorar referencias e texto, colocar - figura sobre Eager vs rendevous 
    - falar sobre escrita independentes e colletiva , vantagens de ambas
    - escritas sincronas e assincronas
    - arquivo compartilhado    
    - acesso continguo vs strides  ( favorece o TWO PHASE I/O )
    - Stripe e OSTs

    - SDDP
        - Introdução - Explicar o que é um cenario.
        - desenhar formato dos dados.
        - arquitetura atual.
        - pipeline SDDP com algoritmo atual
    



    
- Experimentos

    - Ultimos experimentos
    - Tempo total da execução no CSV ( e não somente o bloco de computação )        
    - teste ASYNC AWS , computando tempo de log , sem log block, para confirmar a piora na computacao ( Necessário para escrever menos no capitulo IV)  
    -    teste ASYNC SDUMOMT , computando tempo de log , sem log block, para confirmar a piora na computacao(Necessário para escrever menos no capitulo IV) 

    -  Banda agregada percebida pela aplicação.  (chap 3 ) ? 
    - Comentar que na abordagem central tem uma vantagem, quando o numero de nós e pequena, porque boa parte da carga de trabalho usa comunicação Intra node. 
    - por que stripe de 1 MB ? 
   
    - Teste com IOR two phase I/O e banda. 

      - ~~teste ASYNC SDumont ( Falta 32 nós) ~~

- Trabalhos relacionados
    - Buscar trabalhos para relacionados ao problema

- Conclusões e Trabalhos Futuros ( ROMIO )
    - testes com placa de redes infinity band elastic Fabric
    - Teste com diferentes tamanho de stripes 
    - teste com abordagem assincrona para todos os tamanhos.





- JULHO - ARTIGO
    - Modelo analitico
    - Validação com IOR



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
