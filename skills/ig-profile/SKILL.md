---
name: ig-profile
description: >-
  Dá nota de 0 a 100 pra um perfil do Instagram numa rubrica de 12 itens e
  reescreve as partes que perdem ponto: campo de nome, bio, link, destaques,
  os três fixados, grid. Use quando o usuário disser "otimiza meu perfil",
  "arruma minha bio", "dá nota pro meu Instagram", "por que ninguém me segue",
  ou colar o perfil e perguntar como ele soa.
---

# ig-profile

Quase todo mundo otimiza a coisa errada aqui. O perfil não é uma vitrine que
as pessoas passeiam. É uma **tela de decisão**, a que se chega por um reel, e
tem uns três segundos pra responder uma pergunta: tem mais disso aqui, e é pra mim?

## Entrada

Peça pro usuário colar ou mandar print de: o campo de nome, o @, a bio, pra
onde vai o link, os nomes dos destaques, o que está fixado, e as nove primeiras
capas do grid. Um print do topo do perfil mais as duas primeiras linhas do grid
basta pra primeira passada.

Não faça login no Instagram pelo usuário.

## Dê a nota

Leia `rubric.json` nesta pasta (mesma pasta deste SKILL.md). Doze itens, 100
pontos, cada um com o que é nota cheia e como costuma falhar. Dê nota a cada
item, mostre a tabela, dê o total. Seja honesto. A maioria dos perfis fica na
faixa dos 30 e 40 na primeira passada, e nota generosa não serve pra nada.

```
NOTA DO PERFIL  38/100

  campo de nome     2/12   só o nome, nenhuma palavra que alguém pesquisa
  1ª linha da bio   3/12   três substantivos e um emoji de café
  3 fixados         0/10   nada fixado
  destaques         2/8    "Aleatório", "Vida", "2023"
  grid legível      4/8    seis das nove capas são um rosto no meio de uma frase
  ...
```

## Depois reescreva, nessa ordem

Corrija do item que mais perdeu ponto pro que menos perdeu. Não reescreva tudo
de uma vez: o usuário tem que ir lá mudar cada um.

**1. O campo de nome (30 caracteres).** A linha em negrito embaixo da foto, não
o @. É o campo que a busca do Instagram lê, e a maioria das contas põe só o
nome. Formato que funciona: `{Nome} | {o que faz, em palavras buscadas}`. Dê
três opções.

**2. Primeira linha da bio.** Pra quem é e o que muda. Não é cargo, não são
adjetivos, não é lista de identidades separada por barra. O resto dos 150
caracteres traz uma prova ou uma oferta simples.

**3. Os três fixados.** Três posições, três funções: a melhor prova, a
explicação mais clara da oferta, a melhor apresentação da pessoa. É a correção
de maior alavanca do perfil todo e leva quatro toques. Grid sem fixado mostra
o que foi postado por último, que é cara ou coroa.

**4. Destaques.** Quatro a seis, com nome das perguntas que um comprador faz:
Preços, Resultados, Como funciona, Sobre. Não "Aleatório". Apague o resto.

**5. O link.** Um destino que combina com o que a bio acabou de prometer. Pode
ter até cinco; dois já é cardápio, e cardápio converte pior que porta.

**6. Capas do grid.** As nove primeiras em miniatura. Capa de reel é escolhida,
não o primeiro quadro que veio. Quatro palavras de texto na capa deixam o grid
legível de uma olhada.

## Saída

Tabela de notas, depois as reescritas em blocos prontos pra copiar, na ordem de
correção, cada uma passada pelo `/ig-human`. Dê a nota de novo no final e
mostre a diferença com honestidade. Se a reescrita chega a 84 e não a 98, diga
84, e diga o que falta, que normalmente é grid, hábito de stories e um post
fixado que ainda não existe. Nada disso é reescrita.

Nada é salvo no Instagram por esta skill. O usuário edita cada campo.
