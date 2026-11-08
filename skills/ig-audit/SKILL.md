---
name: ig-audit
description: >-
  Análise do que o usuário já postou: quais reels funcionaram de verdade, por
  quê, e o que parar de fazer. Use quando o usuário colar os insights do
  Instagram ou posts antigos e perguntar "o que está funcionando", "por que
  esse flopou", "lê minhas métricas", "audita meu conteúdo", ou quiser saber do
  que fazer mais.
---

# ig-audit

A única fonte honesta do que funciona pra uma conta é a própria conta. Toda
regra de todo guia de Instagram, incluindo as deste pacote, é um palpite
inicial. Os últimos 30 posts do usuário são a evidência.

## Entrada

Peça o que o usuário tiver:

- Insights por post: views, alcance, interações, tempo de exibição,
  salvamentos, compartilhamentos, seguidores ganhos, e a fatia do alcance que
  veio de não seguidores. Print serve.
- Ou o gráfico de retenção do melhor e do pior reel recente. Esse print sozinho
  vale mais que todo o resto junto.
- Ou só os posts e as views, que já dá pra uma primeira passada.

Leia também `~/.claude/instagram/log.md` se existir, porque ele registra a
fórmula de gancho de cada post.

## O que medir de verdade

View bruta é o número menos útil da tela, porque depende principalmente de
quantas pessoas já seguem a conta. Calcule isto e mostre a conta:

| métrica | como | o que diz |
| --- | --- | --- |
| **Múltiplo** | views / mediana de views da própria conta | se foi um acerto ou um dia normal |
| **Alcance de não seguidores** | % do alcance de quem não segue | se viajou ou não |
| **Retenção em 3s** | quem ainda estava aos 3s / quem começou | se o gancho funcionou. É a nota do gancho. |
| **Tempo médio de exibição** | direto dos insights | se o meio funcionou |
| **Envios por alcance** | compartilhamentos / alcance | o sinal mais forte que dá pra ganhar. Enviar é a pessoa colocar o nome dela junto. |
| **Seguidores por alcance** | seguidores ganhos / alcance | se o perfil converteu a atenção |

Ranqueie por múltiplo e envios por alcance, não por view. Um reel com 4 mil
views e 90 envios ganhou do que teve 60 mil views e 11.

## Depois, achar o padrão

Com os cinco de cima e os cinco de baixo lado a lado, procure o que separa os
dois grupos, e esteja disposto a concluir algo que o usuário não vai gostar:

- **Retenção em 3 segundos.** Se cima e baixo diferem aqui, é o gancho e mais
  nada, e todo o resto é distração.
- **Fórmula de gancho.** Quais ids do `ig-reel/hooks.json` estão nos cinco de cima?
- **Formato.** Reel, carrossel, imagem única.
- **Duração.** Agrupe em até 15s, 15 a 30s, 30 a 60s, mais de 60s.
- **Tema.**
- **Se o usuário respondeu comentários na primeira hora.**
- **Dia e horário.** Olhe isso **por último** e só se o resto não mostrar nada.
  Quase nunca é a causa, e é onde as pessoas querem que seja.

Diga a conclusão como afirmação com a evidência junto, e diga o grau de
confiança. Com 30 posts dá pra ver padrão. Com 6 não dá, e dizer isso é melhor
que inventar um.

## A distinção que economiza meses

**Reel que tem view e não traz seguidor não é reel ruim, é problema de
perfil.** Reel sem view é problema de gancho. Separe os dois antes de
recomendar qualquer coisa. Se o alcance de não seguidores é alto e seguidores
por alcance é baixo, pare de reescrever gancho e vá pro `/ig-profile`.

## Saída

```
AUDITORIA  ·  31 posts  ·  12/jun - 05/set  ·  mediana de views 4.100

TOP 5 POR MÚLTIPLO
  18,2x  #3  Ninguém Te Conta     74.600 views  62% não seguidores  ret@3s 71%  128 envios
   6,4x  #1  Confissão de Custo   26.300 views  48% não seguidores  ret@3s 64%   71 envios
  ...

ÚLTIMOS 5
   0,3x  #11 Lista Com Favorito    1.200 views   9% não seguidores  ret@3s 31%    2 envios
  ...

O QUE OS DADOS DIZEM
1. Retenção em 3 segundos é a história toda. Os cinco de cima têm média de 66%,
   os de baixo 33%. Todo o resto que te preocupa vem depois dos dois primeiros segundos.
2. Os posts em que quem se deu mal foi você: média de 8,1x contra 0,9x do resto.
   n=5. Sinal mais forte daqui, e não é por pouco.
3. Lista de ferramentas dá view e mais nada. Alcance alto, zero envio, zero
   seguidor. Três dos seus cinco piores.
4. Dia da semana não mostra nada. Terça e sexta estão dentro do ruído. Pare de otimizar isso.

PARAR: listas.
FAZER MAIS: os que têm um custo que você pagou e um número junto.
```

Depois passe as conclusões pro `/ig-plan`, pra próxima semana ser construída
em cima da evidência do próprio usuário e não de padrões, e pro `/ig-viral`,
pra o swipe file ser filtrado pelas fórmulas que funcionam pra essa conta.
