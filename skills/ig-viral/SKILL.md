---
name: ig-viral
description: >-
  Encontra os reels que estão funcionando agora no nicho do usuário, ranqueia
  pelo quanto cada um superou a própria conta, dá nome à fórmula de gancho de
  cada um e transforma isso num swipe file pra gravar. Use quando o usuário
  disser "acha vídeos virais", "o que está funcionando agora", "o que estão
  postando no meu nicho", "faz engenharia reversa desse perfil", "monta um
  swipe file", "por que esse reel bombou", ou perguntar o que gravar e não
  tiver evidência pra responder.
---

# ig-viral

A skill de pesquisa. Todas as outras escrevem; esta vai lá e olha. Rode uma
vez por mês, não todo dia. Fórmula dura uma estação.

## Como rodar o script (leia antes)

Um script mora **na mesma pasta deste SKILL.md**: `swipe.py`. Ele usa também
`../ig-reel/hooks.json` e `../ig-reel/hookscore.py`, então mantenha as pastas
das skills lado a lado. Chame pelo caminho completo, entre aspas. Python:
`python3`; no Windows `python` ou `py`.

```bash
python3 "<pasta desta skill>/swipe.py" coletados.tsv --out ~/.claude/instagram/swipe.md
```

## A única ideia que faz isso valer a pena

**View bruta não é evidência.** Uma conta com dois milhões de seguidores
fazendo 400 mil views teve uma terça fraca. Uma conta com quatro mil seguidores
fazendo 400 mil views achou alguma coisa, e essa coisa dá pra copiar.

Então tudo aqui ranqueia pelo **múltiplo sobre a própria conta**: views
divididas pela mediana recente daquela conta. Acima de 3x é sinal. Abaixo de
1,5x é o dia normal da conta e não ensina nada, por maior que o número pareça.

Colete contas **até umas 10x o tamanho do usuário**. Fórmula que funciona com
2 milhões de seguidores muitas vezes funciona porque tem 2 milhões de seguidores.

## Passo 1: escolher as contas

Peça ao usuário de 6 a 12 contas, ou proponha e peça aprovação:

- **4 diretas** - mesmo nicho, mesma oferta, um pouco à frente.
- **4 vizinhas** - outro nicho, mesmo público. É daqui que se pega formato antes
  de alguém do nicho ter.
- **2 a 4 gigantes** - contas muito maiores, só pra formato, nunca pra
  frequência ou tom.

Peça também pra ele abrir a própria **coleção de Salvos**. É o acervo mais
rápido e relevante que existe e já vem filtrado pelo gosto dele.

## Passo 2: ir lá e olhar

Use a ferramenta de navegação que esta sessão tiver de verdade: navegador
embutido, extensão ligada ao Chrome do usuário, ou controle do computador. Não
tem API pra isso e não precisa, o volume é pequeno o bastante pra ler.

**Regras inegociáveis:**

- **Nunca faça login no Instagram pelo usuário e nunca peça senha.** Se a página
  pede login, quem está logado é o usuário. Use o navegador dele com ele
  presente, ou peça pra ele colar.
- **Isso é ler, não raspar.** Dez contas, uma dúzia de reels cada, em
  velocidade humana. Coleta automática em volume viola os Termos de Uso do
  Instagram e bloqueia contas. Não monte robô, não use serviço de scraping, não
  rode isso em loop em segundo plano.
- **Copie a fórmula, nunca o vídeo.** O formato do gancho, a estrutura, a
  duração, o padrão de cortes. Não o roteiro, não a voz, não a edição. Atribua
  cada linha do swipe file à conta de onde veio.

**O que anotar por reel**, nas palavras do criador:

| campo | observação |
| --- | --- |
| conta | o @ |
| seguidores | do perfil |
| mediana | olhe os últimos 12 reels e pegue a view do meio |
| views | deste reel |
| gancho | a primeira frase, falada ou na tela, literal, com erro e tudo |
| na tela | a primeira cartela, se for diferente |
| duração | segundos |
| cta | o que pediu no final |

A mediana é a importante. Sem ela você volta a ranquear por seguidor, que é
exatamente o que esta skill existe pra impedir.

**Quando o Instagram não mostra o suficiente:** a mesma gramática de gancho
roda no YouTube Shorts, onde view e transcrição são públicas e não precisa de
login. É um segundo acervo legítimo, e o gancho falado é mais fácil de pegar
(precisa do `yt-dlp` instalado: `pip install yt-dlp`):

```bash
# views dos shorts de um canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@CANAL/shorts" > canal.json

# a primeira frase falada de um short, pelas legendas automáticas
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "pt.*,en.*" --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DO_VIDEO"
```

Pegue toda palavra da legenda com tempo abaixo de 3,0 segundos. Esse é o
gancho como foi dito, não como foi escrito.

## Passo 3: ranquear

Preencha um arquivo separado por TAB com cabeçalho (em português ou inglês) e
rode o script. Aceita "48 mil", "1,2 mi", "412.000":

```
conta	seguidores	mediana	views	gancho
@alguem	48000	11000	412000	ninguém te conta que seus primeiros 30 reels vão flopar
```

Ele calcula o múltiplo, dá nome à fórmula usando as mesmas 26 do `/ig-reel`
(reconhece ganchos em português e inglês), dá nota a cada gancho com o
`hookscore.py` e mostra o que separa o terço de cima do terço de baixo.

## Passo 4: dizer o que significa, com cuidado

Relate três coisas e mais nada:

1. **Quais fórmulas aparecem mais** no terço de cima, com contagem. Duas
   fórmulas aparecendo quatro vezes cada em seis contas é descoberta. Uma
   aparecendo duas vezes não é.
2. **O que o terço de cima tem em comum na estrutura** que o de baixo não tem:
   tamanho do gancho, se a entrega é visual, se o primeiro quadro se mexe, onde
   fica o pedido.
3. **As linhas "sem nome".** Todo gancho que o classificador não reconheceu é
   ruído ou uma fórmula que ainda não está no `hooks.json`. Leia à mão. É a
   coluna mais valiosa da saída e é por isso que o script mostra a contagem.

Depois diga o tamanho da amostra e a confiança em palavras simples. Quarenta
reels em seis contas sustentam uma afirmação. Doze não, e dizer isso é a
diferença entre pesquisa e horóscopo.

## Passo 5: virar algo pra gravar

Pras três fórmulas do topo, escreva **a versão do usuário**: a história dele, o
número dele, no formato que está funcionando. Passe cada uma pro `/ig-reel`
com a fórmula já escolhida.

Nunca devolva "faz um reel igual esse". Devolva uma frase de gancho que ele
poderia falar amanhã.

## Saída

```
SWIPE  ·  38 reels  ·  7 contas  ·  base: mediana da conta

FORA DA CURVA (acima de 3x)
  38,4x  gancho 86  #3  Ninguém Te Conta   @conta_a    412.000  (mediana 10.700)
  11,2x  gancho 79  #9  Rouba Isso         @conta_c    180.000  (mediana 16.100)
  ...

O QUE ESTÁ APARECENDO MAIS
  #3 Ninguém Te Conta   x5 no terço de cima, 0 no de baixo
  #2 Ordem Negativa     x4
  tamanho do gancho     8 palavras em cima, 19 embaixo

SEM NOME (6)
  Dois desses têm o mesmo formato e ele não está no hooks.json: um gancho que
  abre lendo em voz alta o comentário de outra pessoa. Vale adicionar.

SUA VERSÃO
  #3  "Ninguém te conta que as primeiras 20 propostas são pra perder."
  ...
```

Salve o swipe file em `~/.claude/instagram/swipe.md`. O `/ig-reel` e o
`/ig-plan` leem esse arquivo, e esse é o ponto: depois de rodar uma vez, o
resto do pacote trabalha com a evidência do próprio usuário em vez de padrões.

Nada é postado, seguido, curtido ou mandado por esta skill. Ela lê.
