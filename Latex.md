# Compilacao do PDF

Este projeto foi compilado manualmente porque o `latexmk` do MiKTeX nao conseguiu executar sem Perl instalado.

Arquivo principal:

```powershell
dissertacao.tex
```

PDF gerado:

```powershell
dissertacao.pdf
```

## Sequencia executada

Execute os comandos abaixo na raiz do projeto:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error dissertacao.tex
bibtex dissertacao
makeindex -s coppe.ist -o dissertacao.los dissertacao.syx
makeindex -s coppe.ist -o dissertacao.lab dissertacao.abx
pdflatex -interaction=nonstopmode -halt-on-error dissertacao.tex
pdflatex -interaction=nonstopmode -halt-on-error dissertacao.tex
```

## Observacoes

- A primeira passada do `pdflatex` gera o PDF inicial e atualiza os arquivos auxiliares.
- O `bibtex` atualiza a bibliografia a partir de `bibliografy.bib`.
- Os dois comandos `makeindex` atualizam, respectivamente, a lista de simbolos e a lista de abreviacoes usadas pela classe COPPE.
- As passadas finais do `pdflatex` estabilizam referencias cruzadas, sumario, lista de figuras, lista de tabelas, citacoes e bookmarks.
- Avisos de `Underfull \hbox` podem aparecer e normalmente indicam apenas problemas menores de quebra/justificacao de texto.
- Durante a compilacao atual, o BibTeX reportou avisos de `journal` vazio em algumas entradas bibliograficas, mas isso nao impediu a geracao do PDF.

## Comando alternativo

Se Perl estiver instalado e o `latexmk` estiver funcionando, a compilacao equivalente pode ser feita com:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error dissertacao.tex
```
