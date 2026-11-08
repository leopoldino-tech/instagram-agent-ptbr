---
name: ig-caption
description: >-
  Escreve a legenda do Instagram (a linha que sobrevive ao corte do "... mais",
  o corpo, o pedido único, os termos de busca e até cinco hashtags) e revisa
  antes de sair. Use quando o usuário disser "escreve a legenda", "legenda pra
  esse reel", "o que eu coloco na descrição", tiver um reel ou carrossel pronto
  e precisar do texto, ou perguntar sobre hashtag.
---

# ig-caption

## Como rodar o script (leia antes)

Um script mora **na mesma pasta deste SKILL.md**: `caption.py`. Chame pelo
caminho completo da pasta da skill, entre aspas. Python: `python3`; no Windows
`python` ou `py`. Salve a legenda num `.txt` em UTF-8 e passe o caminho.

```bash
python3 "<pasta desta skill>/caption.py" legenda.txt
python3 "<pasta desta skill>/caption.py" legenda.txt --keywords "edição de vídeo,contrato freelancer"
```

Ele imprime a legenda do jeito que o feed imprime: os primeiros 125 caracteres
numa caixa, o resto atrás do toque. Leia essa caixa antes de qualquer outra
coisa que você escreveu.

## Primeiro, decida qual é o trabalho dessa legenda

Essa é a decisão que estraga legenda quando é pulada.

**Trabalho A: o vídeo já fisgou.** O Reel tem o próprio gancho nos dois
primeiros segundos, falado e na tela. A legenda não é um segundo gancho, e
competir com o vídeo é como perder os dois. O trabalho dela é o pedido, o
contexto que faz o pedido fazer sentido, e as palavras que as pessoas buscam.

**Trabalho B: a legenda é o conteúdo.** Foto, imagem única, capa de carrossel
que abre uma curiosidade. Aqui a linha 1 é o gancho e funciona igual gancho de
Reel: concreto, curto, cortado num suspense e não no meio de uma oração.

Pergunte qual dos dois. Se o usuário tem um Reel com gancho forte, escreva A e
diga por quê.

## O formato

```
Linha 1     125 caracteres visíveis. Trabalho A: o pedido, direto.
            Trabalho B: o gancho.
            Nunca cumprimento ("oi gente"), nunca hashtag, nunca emoji como
            primeiro caractere.
Corpo       parágrafos curtos, uma linha em branco entre eles. Dois a seis.
            É aqui que moram os termos de busca.
O pedido    um. Comentar uma palavra, salvar ou chamar na DM. Um.
Hashtags    até cinco, na própria linha no final, ou nenhuma.
```

O limite é 2.200 caracteres e quase nada precisa de 2.200. Uma legenda que
ganha o toque e entrega 600 caracteres ganha de uma que entrega 1.800.

## Hashtag, sendo honesto

Hashtag não é mais alavanca de alcance, e a plataforma disse isso com uma
mudança de produto. Segundo o anúncio da conta @Creators, **o Instagram limitou
hashtags a cinco por post em 18 de dezembro de 2025** (antes eram trinta),
dizendo que usar poucas e específicas funciona melhor que muitas genéricas.
Regra de plataforma muda: se o Instagram mudar de novo, quem manda é ele, e o
número fica em `HASHTAG_LIMIT` no `caption.py`.

Então: até cinco, específicas, como etiqueta de assunto. Se o usuário tem um
bloco de vinte salvo no bloco de notas, esse bloco é peso morto e o revisor vai
reprovar.

`#viral`, `#fyp`, `#explore`, `#paravoce`, `#reels`, `#sucesso` não descrevem
nada. Corte.

## Termo de busca vale mais que hashtag hoje

A busca do Instagram lê o texto da legenda. Então a frase pela qual o usuário
quer ser achado entra na legenda como alguém digitaria, numa frase que soa
normal. "Edição de vídeo" como palavras na linha três, não "#edicaodevideo"
num bloco no final.

Peça dois ou três desses termos e passe pro revisor com `--keywords`.

## Regras

- **Sem link na legenda.** Legenda não é clicável. URL no texto é texto morto
  que diz "eu não uso essa plataforma". Bio ou DM.
- **Um pedido.** Dois pedidos é o mesmo que nenhum. O `caption.py` conta.
- **O pedido de palavra-chave precisa de uma palavra que dá pra digitar.** Uma
  palavra, sem espaço, sem emoji, e fale ela no vídeo também. `Comenta
  CONTRATO` funciona. `Comenta "o guia do contrato"` não.
- **Escreva o primeiro comentário separado** se tiver link. Diga isso no recibo.
- **Emoji como pontuação, não enfeite.** O revisor aponta acima de 4 a cada
  100 caracteres.
- **Texto alternativo vale 20 segundos.** Pra carrossel e foto, escreva. Leitor
  de tela e o Instagram leem.

## O fluxo

1. Decida Trabalho A ou B e diga qual.
2. Escreva o rascunho.
3. Passe pelo `/ig-human`. Legenda é curta, então vocabulário de IA aparece
   mais aqui do que em qualquer outro lugar.
4. Rode `caption.py` com os termos de busca do usuário. Corrija toda FALHA.
   Decida em voz alta sobre cada ATENÇÃO, em vez de ignorar calado.
5. Entregue o bloco pronto pra copiar, depois o recibo:

```
LEGENDA PRONTA
trabalho:   A - o reel carrega o gancho
visível:    118 de 125 caracteres usados antes do corte
pedido:     um, comenta CONTRATO
hashtags:   3
busca:      "edição de vídeo" na linha 3, "contrato freelancer" na linha 5
revisor:    PRONTA
```

Nada é postado. O usuário cola.
