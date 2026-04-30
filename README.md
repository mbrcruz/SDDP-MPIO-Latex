# Dissertação — projeto LaTeX (CoppeTeX)

Projeto migrado do paper IEEEtran (`sbaconf.tex`) para o template
**CoppeTeX** (PESC/COPPE/UFRJ), versão atual em `D:\Marcelo\Projetos\CoppeTeX`.

## Estrutura

| Arquivo                       | Descrição                                            |
|-------------------------------|------------------------------------------------------|
| `dissertacao.tex`             | Arquivo principal — começa por aqui                  |
| `bibliografy.bib`             | Referências (placeholders TODO — substituir)         |
| `coppe.cls`                   | Classe LaTeX da COPPE                                |
| `coppe-unsrt.bst`             | Estilo de bibliografia (autor-ano, ordem de citação) |
| `coppe-plain.bst`             | Alternativa: autor-ano, ordem alfabética             |
| `en-coppe-{unsrt,plain}.bst`  | Versões em inglês (caso troque `[english]`)          |
| `coppe.ist`                   | Estilo do `makeindex` (lista de símbolos/abrev.)     |
| `coppe-logo.{pdf,eps}`        | Logos                                                |
| `latexmkrc`                   | Receita do `latexmk` (Overleaf usa automaticamente)  |
| `*.png`                       | Figuras referenciadas no texto                       |

## Compilação

### Overleaf
1. Compilador: **pdfLaTeX** ou **LuaLaTeX**.
2. Arquivo principal: `dissertacao.tex`.
3. O Overleaf detecta o `latexmkrc` automaticamente — listas de símbolos
   e abreviaturas são geradas sem passos manuais.

### Linha de comando (TeX Live / MiKTeX)
```bash
latexmk -pdf dissertacao.tex
```
Para forçar a regeneração das listas:
```bash
latexmk -C
latexmk -pdf dissertacao.tex
```

## Pendências identificadas no texto
Procure por `ToDp` ou `ToDO` em vermelho no `.tex`:
- Expandir parágrafo sobre paradigma de simulação na Introdução
- Apresentar a organização da dissertação ao fim da Introdução
- Detalhar o algoritmo SDDP e sua E/S atual
- Inserir figura "cenários × estágios"
- Redigir Agradecimentos
- Preencher placeholders de orientador(es) e examinadores no preâmbulo
- Substituir entradas TODO em `bibliografy.bib` por referências reais

## Estilo de citação
Sem opção `[numbers]` na `\documentclass`, `natbib` usa **autor-ano**
(`Pereira & Pinto, 1991`). Para alternar para numérico (`[1]`), edite a
linha:
```latex
\documentclass[msc,numbers]{coppe}
```

## Idioma
Texto principal em português. Para mudar para inglês, use:
```latex
\documentclass[msc,english]{coppe}
\bibliographystyle{en-coppe-unsrt}
```
"# SDDPMPIIOLatex" 
# SDDP-MPIO-Latex
