## Correções pequenas

- introdução 
             
    - Por que não paralelização da leitura.
    - importancia de usar mais cenários.
    - aquecimento global X aumento saidas
    - Não mexer no padrão de acesso.

- Trabalhar no capitulo III 

    - RING 32 
    
    - possivel break rendevous e eager em 128KB
    - AGregadores pode aumentar o consumo de memoria
    - Deadlock com two phase E/S - mais escritas no necessarios e numero de cenarios desalinhado por processo
    - Validação dos dados: formato arquivos
    -- migrar : Considerações de conguração
    - ~~BUFFERING de registros~~
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
    - Não destacar ambiente em nuvem , substituir por  ambiente computacional e criar sessão AWS para falar as configurações e SDumont também . 
    - Bag-of-tasks
    - ~~MPI (  MPI-IO ) sendo uma unica seção - Melhorar referencias e texto, colocar - figura sobre Eager vs rendevous ~~
    - ~~falar sobre escrita independentes e colletiva , vantagens de ambas~~
    - ~~escritas sincronas e assincronas~~
    - arquivo compartilhado    
    - Acesso continguo vs strides  ( favorece o TWO PHASE I/O )
    - Melhorar explicação sobre o Lustre na fundamentação teórica
        - Stripe e OSTs
    - SDDP
        - Introdução - Explicar o que é um cenario.        - 
        - arquitetura atual.
        - Comparar formato dos resultados horário e por bloco.
        - pipeline SDDP com algoritmo atual


- Experimentos

    - Colocar os experimentos sincronos
    - intervalo de confiança stddev ?    
    - novo histograma de blocos de dados    
    - 117 arquivos ( sendo 104 arquivos horarios e 13 diarios ), tendo os formato de arquivos diarios , será necessário mudar esse padrão de acesso para reduzir o numero de ida ao Lustre.                        
    - Ultimos experimentos ( ASYNC RING 32 ) - Testes ASYNC SDUMOMT , computando tempo de log , sem log block, movendo wait para o final
    - IOR - teste de diferentes de tamanhos de strip com caso reduzido para orientar a decisão do tamanho dos stripes - Por que stripe de 1 MB?        
    - bind-to core
    - Stripe count  
    - Banda agregada percebida pela aplicação
    - Comentar que na abordagem central tem uma vantagem, quando o numero de nós e pequena, porque boa parte da carga de trabalho usa comunicação Intra node.         
    - ~~Tempo total da execução no CSV ( e não somente o bloco de computação )~~
    - ~~teste ASYNC AWS , computando tempo de log , sem log block,para confirmar a piora na computacao ( Necessário para escrever menos no capitulo IV)~~
    - ~~teste ASYNC 4 OSTS~~
    - ~~Metodologia dos experimentos e intrumentação~~


- Trabalhos relacionados
    - Buscar trabalhos para relacionados ao problema

- Conclusões e Trabalhos Futuros ( ROMIO )
    - RING 3 foi suficiente para praticamente zerar o tempo de wait
    
    - AWS demora para muitos nós na mesma zona de disponiilidade.
    - fila SDumont

    - AWS: 36,7% de redução no tempo total em 32 nós;
    - AWS: 113× ganho de banda percebida;
    - SDumont: 43,0% de redução no tempo total em 32 nós;
    - SDumont: 13,7× ganho de banda percebida;
    - impacto de 4 vs 10 OSTs.
    -As siversas escritas de blocos menores estão associados com um padrão de arquivos diarios, poucos arquivos estão nesse formato e que escreve um registro por dia do mês, os dias não foram agrupados como no arquivo horario, embora ter sido mitigado com sobreposição de E/S/COmputação.
    - 117 arquivos (sendo 104 arquivos horarios e 13 diarios ), tendo os formato de arquivos diarios , será necessário mudar esse padrão de acesso para reduzir o numero de ida ao Lustre. 
    - Problema de disponibilidade de instancias na mesma região na AWS
    - Testes com placa de redes infinity band elastic Fabric
    - Teste com diferentes tamanho de stripes .
    - teste com abordagem assincrona para diferentes tamanho de blocos de dados.
    - teste com two phase E/S para avalia se a coordenação - os testes diveram dead lock por ter mais escritas por cenário e também com desalinhamento do numero de cenarios por processo. 







- Revisão orientadores

    - Verificar conjugação verbal

- introdução 
    - amplamente adotado em supercomputadores listados no
    TOP500
    - Tirar uso pelo ONS e avisar que o SDDP é desenvolvido pela PSR , sendo o modelo oficial em x paises  
    - cada cenário resolvido tem seu bloco de resultados enviado, via
MPI_Send, ao processo escritor, 

-Capítulo 3

- ~~Diagrama coordenação MPI-IO Open/Close ~~
- ~~E Numerar os cenários , tirar os azuis - ok~~ 
- ~~Figura OSTs - implementação ok~~
- Explicação sobre Arquivo diarios e RING 32
- Melhorar explicações da implementação figura 3.2  - Antes e no label  da escrita , acertar open antes da primeira escrita. 
- Pseudo código da implementaçãoS
- Configuração como sumário do capítulo 3





