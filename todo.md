## Correções pequenas

- introdução 
    - Tirar uso pelo ONS e avisar que o SDDP é desenvolvido pela PSR , sendo o modelo oficial em x paises

- Trabalhar no capitulo III 

    - RING 4 
    - BUFFERING de registros    - 
    - possivel break rendevous e eager em 128KB
    - AGregadores pode aumentar o consumo de memoria
    - Deadlock com two phase E/S - mais escritas no necessarios e numero de cenarios desalinhado por processo
    - Validação dos dados: formato arquivos
    - ~~Formato dados~~
    - ~~Falar como que foi implementado com escrita assincrona para blocos até 128K e sincrona para blocos maiores  ( Mencionar Eager e Rendevous ) - minimzar pressão pelo uso de memoria.~~
    - Processo Gerenciador de tarefas";    
    - ~~Fortan,C/C++,Mosel~~   
    - ~~Introdução da arquitetura proposta~~
    - ~~Visão geral e explicação da arquitetura proposta.~~
    - ~~novo pipeline SDDP - execução ,  escrita , reeexução , reescrita de dados e independencia de processos.~~  
    - ~~Relacionar com arquivos compartilhados - blocos de dados separados em OSTs~~
    - ~~Apresentar o modelo de Escrita independente E/S , e dizer porque não foi selecionado a escrita coletiva que precisa de um certa coordenação entre os processos, pois o SDDP funciona resolver problemas indepentes e sincronizacao de escrita pode ser prejudicial neste casp.~~
    - ~~Mostrar como os arquivos são distribuidos em stripes.~~   
    - Equação explícita do offset. A descrição em prosa (l. 234–239) é defensável, mas uma equação tornaria a proposta verificável. Custo: 4 linhas.
    - Limiar 128 KB sem ancora empírica (Subseção 3.3.2, l. 178–186). Vale citar o histograma do Cap. 4 (Fig. 4.1, fig:histograma_mensagens) — a justificativa empírica está pronta para uso, é só ligar.
    - \paperwidth em três figuras (l. 42, l. 89, l. 145). As três usam \includegraphics[width=0.95\paperwidth], o que faz a figura sangrar para fora da área de texto. Convenção COPPE pede \textwidth. Confira no PDF compilado se o efeito é intencional.
    - Ponte para Cap. 4 no fim da Seção 3.4. Falta apontar quais valores de stripe_count foram adotados nos experimentos (10 AWS, 6 SDumont, ambos com stripe_size = 1MB).
    Caption da Fig. 3.3 ainda genérica (l. 147): "Formato lógico dos arquivos binários de resultado do SDDP." — pode ganhar uma frase descritiva.
    
    


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
        - Introdução - Explicar o que é um cenario.        - 
        - arquitetura atual.
        - Comparar formato dos resultados horário e por bloco.
        - pipeline SDDP com algoritmo atual
        -
- Introdução
    - Por que não paralelização da leitura.
    - importancia de usar mais cenários.
    - aquecimento global X aumento saidas

    



    
- Experimentos

        - IOR - teste de diferentes de tamanhos de strip com caso reduzido para orientar a decisão do tamanho dos stripes ???Por que stripe de 1 MB?                
        - ~~Ultimos experimentos ( ASYNC ) Testes ASYNC SDUMOMT , computando tempo de log , sem log block, movendo wait para o final (Necessário para escrever menos no capitulo IV)~~
        - ~~Metodologia dos experimentos e intrumentação~~
        - ~~bind-to core~~
        - ~~Banda agregada percebida pela aplicação.~~
        - ~~Comentar que na abordagem central tem uma vantagem, quando o numero de nós e pequena, porque boa parte da carga de trabalho usa comunicação Intra node.~~
        
        
        - ~~Stripe count~~        
        - ~~Tempo total da execução no CSV ( e não somente o bloco de computação )~~
        - ~~teste ASYNC AWS , computando tempo de log , sem log block,para confirmar a piora na computacao ( Necessário para escrever menos no capitulo IV) ~~
        - ~~teste ASYNC 4 OSTS~~
        
   
    - Teste com IOR two phase I/O e banda. 
    - ~~teste ASYNC SDumont ( Falta 32 nós) ~~

- Trabalhos relacionados
    - Buscar trabalhos para relacionados ao problema

- Conclusões e Trabalhos Futuros ( ROMIO )
    - RING 4 foi suficiente para praticamente zerar o tempo de wait
    - Consumo de memoria e possiveis soluções, impediu uso de hiper threading
    - fila SDumont
    - mesmo com bufferização alguns arquivos ficaram intervead , por teria apenas 1 registro por cenário e estagio e apresentou blocos muito muito menores, embora ter sido mitigado com sobreposição de E/S/COmputação.
    - 117 arquivos, tendo varios arquivos 
    - Problema de disponibilidade de instancias na mesma região na AWS
    - testes com placa de redes infinity band elastic Fabric
    - Teste com diferentes tamanho de stripes 
    - teste com abordagem assincrona para todos os tamanhos.
    - teste com two phase E/S para avalia se a coordenação - os testes diveram dead lock por ter mais escritas por cenário e também com desalinhamento do numero de cenarios por processo. 





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
