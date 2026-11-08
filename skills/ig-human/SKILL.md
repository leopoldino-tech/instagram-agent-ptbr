---
name: ig-human
description: >-
  Tira a "cara de IA" de qualquer texto (travessão, vocabulário de ChatGPT,
  caracteres invisíveis) e dá nota num painel de cinco checagens antes de
  sair. Use sempre que um texto precisar soar humano, quando o usuário disser
  "humaniza", "isso tá com cara de IA?", "tira os travessões", "tá parecendo
  ChatGPT", "deixa mais natural", e antes de mostrar qualquer legenda, roteiro,
  comentário, resposta ou DM ao usuário. Funciona em português e inglês.
---

# ig-human

## Como rodar os scripts (leia antes)

Dois scripts moram **na mesma pasta deste SKILL.md**: `humanize.py` e
`detect.py` (e o auxiliar `langdetect_ig.py`, que eles importam). Eles rodam
de verdade. Use, não olhe no olho.

- Sempre chame pelo **caminho completo da pasta desta skill**, entre aspas.
- Python: tente `python3`. No Windows use `python` (ou `py`). Python 3.8+,
  sem instalar nada.
- Salve o rascunho num `.txt` em UTF-8 numa pasta temporária e passe o caminho.
  O idioma é detectado sozinho; force com `--lang pt` se o texto for muito curto.

```bash
python3 "<pasta desta skill>/humanize.py" rascunho.txt -o limpo.txt --report  # limpa e mostra o que mudou
python3 "<pasta desta skill>/detect.py" rascunho.txt                          # nota, cinco checagens
python3 "<pasta desta skill>/detect.py" rascunho.txt limpo.txt                # prova o antes e depois
```

Os dois leem `slop.json`: um bloco em inglês (o original) e um bloco em
português com o vocabulário de IA que aparece em legenda brasileira:
"alavancar", "crucial", "no mundo atual", "vale ressaltar que", "próximo
nível", "para de rolar", "o algoritmo ama", "me segue para mais dicas". Cada
entrada tem uma troca simples. O arquivo é feito pra ser editado: se o usuário
usa de verdade uma palavra que a lista troca, apague a entrada.

## Por que isso pesa mais no Instagram

Legenda é curta e roteiro é falado. Uma frase com cara de redação numa legenda
de 600 caracteres ocupa uma fatia maior do texto que numa redação, e uma
locução que ninguém falaria naturalmente aparece no primeiro take. O problema
aqui não é um detector marcando o post. É uma pessoa passando reto por algo
que soa como marca, ou o criador tropeçando no próprio roteiro.

## O que é corrigido sozinho

**1. Caracteres invisíveis.** Zero-width, word joiner, hífen suave, BOM,
caracteres de tag Unicode, espaços não separáveis. Teclado não produz isso.
Sobrevivem ao copiar e colar e são invisíveis em qualquer editor. Exceção: o
joiner dentro de emoji composto (👨‍👩‍👧) é preservado, senão o emoji quebra.

**2. Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
viram retas, reticências (…) viram três pontos, marcador (•) vira hífen.

**3. Vocabulário de IA.** Cada termo trocado por uma palavra simples ou
apagado, mantendo maiúsculas e sem mexer em links.

## O que NÃO é corrigido sozinho

Padrões de estrutura são **apontados, não reescritos**, porque mudar o formato
de uma frase pede julgamento:

- "Não é só X, é Y" e "não só X, mas também Y"
- "Isso não é sobre X. É sobre Y."
- Tríades (lista de três)
- Linha de pergunta retórica: "O resultado?"
- Preâmbulo de vídeo: "nesse vídeo eu vou te mostrar"
- Lista com emoji de marcador (✅ ✅ ✅)
- Três ou mais palavras GRITADAS seguidas
- Parede de hashtags (6+)
- Isca reflexa: "me segue", "marca alguém", "deixa seu like"
- "Em resumo," abrindo parágrafo

Essa lista é trabalho seu. Reescreva cada linha apontada à mão, mantendo o
sentido, e rode o `detect.py` de novo. É isso que leva a nota de REVISAR pra
PASSOU, e é a parte que script nenhum faz.

## As cinco checagens

`detect.py` dá nota 0-100 pra cinco sinais, maior é mais humano:

| checagem | o que mede | máquina parece |
| --- | --- | --- |
| VARIAÇÃO | variação no tamanho das frases | toda frase do mesmo tamanho |
| CONCRETUDE | números, nomes, valores a cada 100 palavras | substantivo abstrato, sem número |
| VOCAB. IA | termos prontos a cada 100 palavras | vocabulário de ChatGPT |
| DIGITAL | invisíveis, travessões, aspas curvas a cada 1k caracteres | tipografia perfeita demais |
| VOZ | marcas de fala ("pra", "tá", "a gente"), pessoa, padrões | sem fala, revelações encenadas |

O veredito pesa a média em 60% e a **checagem mais fraca** em 40%, porque um
sinal só já basta. PASSOU precisa de 70+ no geral e nenhuma checagem abaixo de 55.

## Diga isso com honestidade

São cinco heurísticas locais inspiradas nos sinais que detectores públicos
usam. Rodam na máquina do usuário e nada é enviado. **Não são** GPTZero,
Originality, Copyleaks, Winston nem Turnitin, não chamam essas APIs e não
prometem o veredito delas. Consertar o que elas medem tende a mexer nesses
números, porque medem as mesmas coisas. Essa é a promessa. Não faça uma maior
em nome do usuário e nunca diga que o texto é "indetectável".

## Ordem das operações

1. `humanize.py rascunho.txt -o limpo.txt --report`
2. Leia os padrões de estrutura apontados. Reescreva essas linhas você mesmo.
3. `detect.py rascunho.txt limpo.txt` pra mostrar antes e depois.
4. Se não deu PASSOU, conserte a checagem mais fraca citada na saída e rode de
   novo. Duas rodadas é normal. Cinco quer dizer que o rascunho foi escrito por
   fórmula, e a solução é outro rascunho, não mais rodadas.
5. Mostre ao usuário o texto limpo e a nota. Nunca só a nota.
