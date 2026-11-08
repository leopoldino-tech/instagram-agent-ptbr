---
name: ig-carousel
description: >-
  Monta um carrossel do Instagram: a capa que faz arrastar, o texto slide a
  slide e os arquivos 1080x1350 pra subir. Use quando o usuário disser
  "carrossel", "slides", "post de arrastar", "transforma isso num carrossel",
  ou tiver uma ideia em forma de lista ou passo a passo que morreria numa
  imagem só.
---

# ig-carousel

Carrossel é o formato do grid que mais segura tempo de tela, porque arrastar é
interação e rolar não é. E ganha uma segunda chance: o Instagram pode mostrar o
carrossel de novo a partir de um slide mais à frente pra quem não interagiu da
primeira vez, então o slide dois também precisa se sustentar sozinho.

O formato premia uma ideia quebrada em passos. Pune legenda picotada em pedaços.

## Quando usar em vez de Reel

Use carrossel quando a ideia tem **sequência e precisa ser relida**: passos, um
método com partes, antes e depois, uma lista que vale print. Use Reel quando a
ideia tem movimento, rosto, ou uma recompensa que precisa ser vista acontecendo.

Se a ideia é uma afirmação só, não é nenhum dos dois. Passe pro `/ig-reel` e diga.

## Estrutura

6 a 10 slides. O limite é 20 e 20 é quase sempre um livro que ninguém termina.
Menos de 5 e o arrastar nem começa.

```
1         CAPA      o gancho. 6 palavras ou menos, num tamanho legível no grid
                    em miniatura. Uma linha de promessa embaixo.
2         O QUE ESTÁ por que isso importa, numa frase. Esse slide é também uma
          EM JOGO   segunda capa, então não pode ser introdução.
3 a N     UMA IDEIA POR SLIDE. Título de 3 a 7 palavras, no máximo 25 palavras
                    embaixo. Se o slide precisa de um parágrafo, são dois slides.
N+1       RESUMO    tudo numa lista. É o slide que as pessoas printam.
ÚLTIMO    CTA       uma ação. Salvar, comentar uma palavra ou seguir. Uma.
```

## Regras do texto

- **A capa é 80% do resultado.** Seis palavras. Grande. Nada no resto salva uma
  capa que ninguém arrasta.
- **Pense no corte do grid.** O grid do perfil corta num retângulo em pé, e a
  proporção exata já mudou mais de uma vez. Monte em 1080x1350 e mantenha o
  texto da capa bem no meio, longe dos 120 pixels de cada borda, e o corte
  deixa de importar.
- **Numere os slides** (3/8). A taxa de conclusão sobe quando a pessoa vê o fim.
- **Nenhum slide é parágrafo.** Se não cabe em 25 palavras, divida.
- **O slide de resumo é o que vai ser printado e mandado.** Envio é o sinal mais
  forte que existe. Faça ele se sustentar sozinho, legível sem contexto.
- **O @ em todo slide**, pequeno, num canto de baixo. Print viaja sem você.
- **Texto alternativo pelo menos na capa.** Leitor de tela e o Instagram leem.

## Gerando os arquivos

O Instagram quer 1080x1350 (4:5), JPEG ou PNG, até 20 itens. Monte em HTML e
exporte cada slide:

```bash
# um <section> por slide, 1080x1350, page-break-after: always
# depois Chrome headless --print-to-pdf, ou qualquer HTML-pra-imagem que você já usa
```

Escreva o HTML com `width:1080px; height:1350px`, uma cor de destaque só, e
fonte nunca menor que 32px, porque isso é lido num celular a um terço do
tamanho real. Se o projeto tem identidade visual ou design system, use e não
invente paleta.

## Saída

Primeiro o texto slide a slide, numa lista numerada que o usuário lê em dez
segundos e edita antes de gerar qualquer coisa. Depois a **legenda**, que pra
carrossel é o Trabalho B do `/ig-caption`: aqui a legenda trabalha, porque a
capa já gastou as seis palavras dela.

Passe os dois pelo `/ig-human`. Gere os arquivos só depois que o usuário
aprovar o texto.

```
CARROSSEL  ·  8 slides

1  CAPA     A CLÁUSULA DE R$ 18 MIL
            Uma linha que hoje vai em todo contrato meu.
2  EM JOGO  Eu aprovei o trabalho. Nove dias depois pediram o dinheiro de volta.
3           O QUE ELA DIZ
            Pagamento na entrega, não na aprovação.
...
7  RESUMO   As quatro linhas, em ordem.
8  CTA      Comenta CONTRATO que eu te mando a cláusula inteira.

Legenda: Trabalho B, gancho na linha 1, um pedido, 3 tags.
```

Nada é enviado. O usuário posta.
