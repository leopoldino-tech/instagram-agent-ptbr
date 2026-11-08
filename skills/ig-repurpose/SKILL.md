---
name: ig-repurpose
description: >-
  Transforma um conteúdo longo (vídeo do YouTube, podcast, live, newsletter,
  artigo ou call com cliente) numa semana de reels e carrosséis. Use quando o
  usuário disser "reaproveita isso", "transforma em reels", "tenho um
  vídeo/podcast/transcrição", "corta isso", ou colar algo longo e quiser levar
  pro Instagram.
---

# ig-repurpose

Um bom conteúdo longo tem quatro a seis posts dentro. A maioria das pessoas
tira um e joga o resto fora.

## Entrada

Uma transcrição, um artigo, uma newsletter, um roteiro, um resumo de call, uma
live. Se o usuário mandar um link e esta sessão tiver ferramenta de
transcrição, use; senão, peça pra colar. Leia tudo antes de extrair qualquer coisa.

Se a fonte é um vídeo do próprio usuário, peça o arquivo também. Reel feito com
o vídeo dele ganha de Reel feito com as palavras dele lidas de novo.

## Extraia, não resuma

Resumo de vídeo não é Reel. Ninguém quer o resumo. Passe pelo conteúdo e puxe
as coisas que se sustentam sozinhas:

| puxar | o que é |
| --- | --- |
| **Afirmações** | toda frase que começaria uma discussão |
| **Números** | todo valor, custo, duração, porcentagem |
| **Histórias** | todo momento com uma pessoa, uma cena e um custo |
| **Mecanismos** | todo "o jeito que isso funciona de verdade é..." |
| **Erros** | toda admissão de algo que deu errado |
| **Frases** | toda frase que já dá pra citar do jeito que está |

Liste o que achou, com contagens, antes de escrever qualquer coisa. Se o
conteúdo rende menos de quatro itens, ele é fraco, e quatro posts espremidos
dele vão ser fracos também. Diga isso.

## Depois escolha o formato de cada extração

Nem tudo é Reel.

- **Afirmação, erro, história** viram Reel. Precisam de voz e rosto.
- **Mecanismo, lista numerada** viram carrossel. Precisam ser relidos.
- **Uma frase citável** vira tela de story, não post.

## Depois monte a semana

Cada extração vira um post e cada post se sustenta completamente sozinho. Quem
assiste não viu a fonte e nunca vai ver. Nunca escreva "como eu falei no meu
último vídeo". O post é a coisa.

Dê uma fórmula de gancho do `ig-reel/hooks.json` pra cada e varie. Cinco posts
de uma fonte com o mesmo formato de gancho parece fábrica de conteúdo, porque é.

Se a fonte é vídeo do próprio usuário, **use o trecho real**. O clipe em que
ele disse a coisa, com a reação de verdade, ganha de regravar toda vez. Corte
na frase, não na respiração.

Ordene na semana assim: a afirmação mais forte primeiro, a história no meio da
semana, e o mecanismo por último, quando quem gostou dos anteriores está esperando.

## Saída

```
FONTE: "Por que a gente acabou com a call de descoberta" (podcast de 42 min, 8.900 palavras)

ACHEI  5 afirmações, 9 números, 3 histórias, 4 mecanismos, 2 erros, 7 frases citáveis

SEMANA
TER  REEL       #2  Ordem Negativa    Para de fazer call de descoberta
                                      use o trecho de 14:20, ele ri no final
QUA  CARROSSEL  legenda Trabalho B    O formulário de 4 perguntas que substituiu a call
SEX  REEL       #21 Começo No Meio    "...e ele pediu reembolso nove dias depois"
DOM  REEL       #5  Tempo Encolhido   Seis horas por semana de volta, um link apagado

Diga "escreve a terça" que eu faço o rascunho.
```

Depois escreva sob demanda, um de cada vez, cada um pelo `/ig-reel` e pelo
`/ig-human`. Não despeje quatro roteiros prontos de uma vez. Vão soar todos
iguais e o usuário não vai gravar nenhum.
