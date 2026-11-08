# Instagram no Claude, em português 🇧🇷

14 skills do Claude que cuidam de um perfil de Instagram. Grátis, código aberto
(MIT), sem cadastro, sem chave de API, sem conectar conta nenhuma.

Uma escreve seu Reel em cima de 26 fórmulas de gancho e **dá nota pro gancho**
antes de você gastar um take nele. Uma vai atrás dos reels que estão
funcionando no seu nicho e ranqueia pelo quanto cada um superou a própria
conta. Uma escreve a legenda e mostra exatamente o que aparece antes do
"... mais". Uma dá nota de 0 a 100 pro seu perfil e reescreve o que perdeu
ponto. Uma planeja a semana.

E uma é o **humanizador**, que é o motivo do resto ser usável. Ele tira os
travessões, o vocabulário de ChatGPT ("alavancar", "crucial", "no mundo
atual", "próximo nível") e os caracteres invisíveis do texto, e depois dá nota
num painel de cinco checagens antes de você ver.

**Nada é postado sem você dizer sim.** Essas skills escrevem. Quem posta é você.

---

## Instalar (escolha um jeito)

Você precisa do **Claude Code** (no app do Claude pra desktop, aba Code, ou no
terminal) e do **Python 3** no computador. Se não sabe se tem Python, pule pra
[Instalar o Python](#instalar-o-python) primeiro.

### Jeito 1: pedir pro Claude instalar (mais fácil)

Cole isto no Claude Code:

```
https://github.com/leopoldino-tech/instagram-agent-ptbr

Instala essas skills pra mim em ~/.claude/skills, roda o verificar.py e me diz se deu certo.
```

### Jeito 2: como plugin

No Claude Code, digite um de cada vez:

```
/plugin marketplace add leopoldino-tech/instagram-agent-ptbr
```

```
/plugin install instagram-ptbr@instagram-ptbr
```

Pra atualizar depois: `/plugin marketplace update instagram-ptbr`.

### Jeito 3: manual

**Windows (PowerShell):**

```powershell
git clone https://github.com/leopoldino-tech/instagram-agent-ptbr.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force instagram-agent-ptbr\skills\ig-* "$HOME\.claude\skills\"
```

**Mac / Linux:**

```bash
git clone https://github.com/leopoldino-tech/instagram-agent-ptbr.git
mkdir -p ~/.claude/skills && cp -r instagram-agent-ptbr/skills/ig-* ~/.claude/skills/
```

Sem `git`? No GitHub clique em **Code → Download ZIP**, descompacte, e copie as
pastas `skills/ig-*` pra `~/.claude/skills/` (no Windows:
`C:\Users\SEU_USUARIO\.claude\skills\`).

> **Importante:** copie as pastas `ig-*` **juntas**. O `/ig-viral` usa arquivos
> do `/ig-reel`, e o `/ig-human` tem um arquivo auxiliar na mesma pasta.

### Conferir se funcionou

Dentro da pasta que você baixou:

```bash
python verificar.py
```

(No Mac/Linux use `python3`.) Tem que aparecer **TUDO CERTO** no final. Se
alguma linha disser FALHOU, manda o print pra quem te passou o pacote.

### Sem Claude Code?

Cole o conteúdo de um `SKILL.md` qualquer no começo de uma conversa no
claude.ai e ele funciona como um "modo". Você perde os scripts em Python (que
são boa parte do valor do `/ig-reel` e do `/ig-human`), mas o resto funciona.

---

## Primeiro passo: `/ig-voz`

Abra o Claude Code e digite **`/ig-voz`**. Mande três reels ou legendas suas
(o texto falado ou escrito). O Claude aprende seu jeito de falar e salva em
`~/.claude/instagram/voice.md`. Todas as outras skills leem esse arquivo.

Isso importa mais no Instagram do que em qualquer lugar, porque você tem que
**falar** as palavras em voz alta. Roteiro na voz errada vira regravação.

---

## As 14 skills

| comando | o que faz |
| --- | --- |
| `/ig-voz` | **Comece aqui.** Aprende seu jeito de falar a partir de 3 textos seus e salva o perfil de voz. |
| `/ig-reel` | Uma ideia vira um Reel. Três ganchos de [26 fórmulas](skills/ig-reel/hooks.json), com nota, depois o roteiro, o texto da tela e os tempos. |
| `/ig-viral` | Vai atrás do que está funcionando no seu nicho, ranqueia pelo múltiplo sobre a mediana de cada conta, dá nome à fórmula e monta o swipe file. |
| `/ig-caption` | A legenda, revisada. Mostra os 125 caracteres que o feed mostra antes do toque. |
| `/ig-carousel` | Carrossel. A capa que faz arrastar, o texto de cada slide, e os arquivos 1080x1350. |
| `/ig-story` | A sequência de stories do dia, qual figurinha faz o quê, e o funil de DM em que a pessoa se mexe primeiro. |
| `/ig-profile` | Nota do perfil numa [rubrica de 12 itens](skills/ig-profile/rubric.json), de 0 a 100, e reescrita na ordem do que mais perde ponto. |
| `/ig-plan` | A semana. O que postar, em qual formato, quando, e as 10 contas pra engajar. |
| `/ig-human` | O humanizador. Dois scripts que rodam de verdade. Veja abaixo. |
| `/ig-comment` | Comentário em post dos outros. Nove tipos, escolhidos pelo que o post é. Nunca "🔥🔥🔥". |
| `/ig-reply` | Os comentários do seu post. Separa em palavra-chave / cliente / conteúdo / pergunta / apoio / ruído, e responde nessa ordem. |
| `/ig-dm` | A entrega da palavra-chave, a primeira mensagem, a proposta de collab e os dois follow-ups. Dois. |
| `/ig-repurpose` | Um vídeo, podcast ou newsletter vira uma semana de reels e carrosséis que se sustentam sozinhos. |
| `/ig-audit` | Análise do que você já postou. Ranqueia por múltiplo e envios por alcance, não por view. |

Você também pode só pedir em português normal ("faz um reel sobre...", "escreve
a legenda", "isso tá com cara de IA?") que o Claude escolhe a skill certa.

---

## As ferramentas que rodam de verdade

Sem dependências, sem internet, nada é enviado. Rodam na sua máquina, no seu
texto, e entendem **português e inglês** (detectam sozinhas). O Claude chama
elas por você; os comandos abaixo são pra quem quiser rodar na mão.

### Gancho e tempo

```bash
python skills/ig-reel/hookscore.py ganchos.txt          # ranqueia suas opções
python skills/ig-reel/beats.py roteiro.txt --target 30  # cronometra antes de gravar
```

```
RANKING DE GANCHOS
==============================================================================
->  84.4 FORTE   Perdi R$ 18 mil por causa de um contrato
        mais fraco: DESTINO (70)
    81.4 FORTE   Ninguém te conta que seus primeiros 30 reels vão flopar
        mais fraco: TENSÃO (70)
    17.0 FRACO   Para de rolar o feed se você quer crescer no Instagram 🔥
        eliminatório: Abre com "para de rolar". Pedir atenção prova que você ainda não ganhou ela.
     9.6 FRACO   Oi gente, hoje eu quero falar sobre estratégia de conteúdo
        eliminatório: Cumprimento. Ninguém abre o feed pra ser cumprimentado.
```

O `beats.py` estima quanto tempo cada linha leva pra ser falada, monta os
timecodes e aponta as quatro coisas que matam um Reel na edição: gancho que
passa de três segundos, trecho longo demais, sequência de linhas sem nada
concreto, e final que não volta pra primeira frase (sem loop).

### A legenda

```bash
python skills/ig-caption/caption.py legenda.txt --keywords "edição de vídeo,contrato"
```

```
  O QUE O FEED MOSTRA
  +------------------------------------------------------+
  | Perdi R$ 18 mil em 2024 porque o contrato não tinha  |
  | uma cláusula. Uma.                                   |
  |                                                      |
  | O cliente aprovou o vídeo, sumiu por nove dias e     |
  | depo                                                 |
  +-------------------------------------------- ... mais +

  OK       PRIMEIRA LINHA    70 caracteres, aparece inteira
  OK       GANCHO CONCRETO   3 número(s) ou nome(s) na parte visível
  OK       HASHTAGS          3 hashtag(s): #freelancer #contratos #editordevideo
  OK       UM PEDIDO SÓ      uma chamada pra ação: comentar uma palavra-chave
```

Aplica o limite atual de **cinco hashtags por post** e reconhece pedido em
português ("comenta CONTRATO", "me chama na DM", "link na bio").

### O humanizador

```bash
python skills/ig-human/humanize.py rascunho.txt --report   # limpa e mostra cada troca
python skills/ig-human/detect.py rascunho.txt              # nota, cinco checagens
python skills/ig-human/detect.py antes.txt depois.txt      # prova a diferença
```

Numa legenda escrita pra ser o pior possível ("Para de rolar o feed! No mundo
atual, é crucial alavancar seu conteúdo de forma robusta..."):

```
  NOTA HUMANA   #######.................  30.2   CARA DE IA
```

Depois do `humanize.py`, sem nem reescrever as estruturas apontadas:

```
  NOTA HUMANA   ##################......  74.8   PASSOU   (+44.6)
```

O vocabulário fica em [`slop.json`](skills/ig-human/slop.json) e é feito pra
ser editado: se você usa uma palavra que a lista troca, apague a entrada.

### O swipe file

```bash
python skills/ig-viral/swipe.py coletados.tsv --out ~/.claude/instagram/swipe.md
```

View bruta não é evidência. Conta de 2 milhões fazendo 400 mil views teve um
dia fraco. Conta de 4 mil fazendo 400 mil achou alguma coisa. O `swipe.py`
ranqueia pelo múltiplo sobre a mediana de cada conta e dá nome à fórmula do
gancho (em português ou inglês).

---

## As letras miúdas, que são a parte honesta

**Essas skills não postam no Instagram.** Existe uma API oficial de publicação
pra conta profissional, mas ela exige app de desenvolvedor na Meta, página
vinculada, token e revisão do app, coisa que uma skill não te entrega. Todo o
resto que as pessoas usam pra automatizar post, comentário, seguir ou DM é
automação de navegador ou ferramenta de terceiros, e as duas coisas violam os
[Termos de Uso do Instagram](https://help.instagram.com/581066165581870) e
bloqueiam contas. Então toda skill aqui termina igual: um bloco pronto pra
copiar, e você posta.

A exceção é resposta automática de palavra-chave na DM, que o Instagram
suporta pelas ferramentas dele e de parceiros aprovados, e que só dispara
depois que a pessoa comenta. O `/ig-dm` explica onde fica essa linha.

**O `/ig-viral` lê, não raspa.** Dez contas, uma dúzia de reels cada, em
velocidade humana, com você usando o seu navegador. Nunca pede sua senha e
nunca entra na sua conta.

**As cinco checagens são heurísticas locais, não detectores.** Não são GPTZero,
Originality, Copyleaks, Winston nem Turnitin, não chamam essas APIs e não
prometem o veredito delas. Ninguém pode te vender "indetectável" com honestidade.

**A nota do gancho pega gancho ruim, não escolhe vencedor.** No teste do autor
original (74 ganchos reais em inglês), ela separa gancho ruim de gancho real
muito bem, mas quase não separa o hit do flop do mesmo criador. Use pra matar
os ganchos fracos antes de gravar e confie no seu gráfico de retenção pro resto.
A versão em português ainda não foi medida num corpus grande; se você testar,
conta o resultado.

**Nada aqui inventa.** Nenhuma métrica, cliente ou resultado inventado vai com
seu nome. Se o rascunho precisa de um número que você não deu, ele volta com
`{{seu número}}` e um aviso.

**Regra de plataforma muda.** O limite de hashtag foi de 30 pra 5 em dezembro
de 2025. Se algo aqui contradiz o que o Instagram está fazendo quando você ler,
o Instagram está certo.

---

## Instalar o Python

**Windows:** abra o PowerShell e rode

```powershell
winget install Python.Python.3.12
```

ou baixe em [python.org/downloads](https://www.python.org/downloads/) e, na
instalação, **marque "Add python.exe to PATH"**. Feche e abra o terminal de
novo e teste com `python --version`.

> No Windows o comando é `python` (ou `py`), não `python3`. As skills já sabem disso.

**Mac:** `python3 --version` no Terminal. Se não tiver, o próprio Mac oferece
instalar, ou use `brew install python`.

---

## O que mudou em relação ao original

Este pacote é uma adaptação do
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
de Jake Schincariol (MIT). O que foi feito:

- **Tudo em português do Brasil**: as 13 skills, os exemplos (R$, contexto
  brasileiro), a rubrica do perfil e os textos das 26 fórmulas de gancho.
- **Os scripts entendem português**: palavras com acento, `R$`, "18 mil", "1,2 mi",
  números por extenso, cumprimentos ("oi gente", "fala galera"), preâmbulos
  ("nesse vídeo eu vou te mostrar") e pedidos ("comenta", "link na bio"). O
  original quebrava palavras acentuadas ao meio.
- **Vocabulário de IA em português** no humanizador (mais de 130 termos novos e
  12 padrões de estrutura), mantendo o bloco em inglês original. O idioma é
  detectado sozinho.
- **Funciona no Windows**: os scripts forçam UTF-8 (o console do Windows
  quebrava com emoji e acento) e as skills explicam `python` vs `python3` e
  chamam os scripts pelo caminho da pasta da skill.
- **Classificador de ganchos bilíngue**: reconhece as 26 fórmulas em português
  (26 de 26 exemplos) sem perder o reconhecimento em inglês do original.
- **Skill nova `/ig-voz`** pra montar o perfil de voz, com o modelo dentro da
  própria skill (no original o modelo ficava fora das skills e não ia junto na
  instalação por plugin).
- **`verificar.py`** pra qualquer pessoa conferir em 10 segundos se a instalação funcionou.
- Correções menores: emoji composto (👨‍👩‍👧) não é mais quebrado pelo
  humanizador, "..." proposital no começo da linha não é apagado, parede de
  hashtag passou a contar a partir de 6 (o limite agora é 5), "Além disso, X"
  vira "E X" em vez de "E, X".

## Créditos

Ideia, estrutura e skills originais: **Jake Schincariol**,
[opusjake.ai](https://opusjake.ai) ·
[repositório original](https://github.com/Jakeschincariol/instagram-agent-skill).

Adaptação para português do Brasil: **Leopoldino** (@leopoldino.z).

## Licença

MIT. Pega, muda, distribui. Só mantenha o arquivo `LICENSE` junto.
