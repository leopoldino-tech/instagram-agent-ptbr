---
name: ig-reel
description: >-
  Escreve um Reel do Instagram a partir de uma ideia crua: opções de gancho
  com base em 26 fórmulas, o roteiro falado, o texto da tela e uma planilha de
  tempos, na voz da pessoa e com nota antes de gravar. Use sempre que o usuário
  quiser um Reel, roteiro de vídeo curto, gancho, locução, "faz um reel sobre
  X", "o que eu falo nesse vídeo", "me dá um gancho", ou vai gravar e ainda não
  tem a primeira frase. Também em inglês: "write a reel", "hook".
---

# ig-reel

Transforma uma ideia crua num Reel que a pessoa assiste até o fim.

## Como rodar os scripts (leia antes)

Dois scripts moram **na mesma pasta deste SKILL.md**: `hookscore.py` e
`beats.py`. Eles rodam de verdade. Use, não chute o gancho nem o tempo.

- Sempre chame pelo **caminho completo da pasta desta skill**, entre aspas
  (o caminho pode ter espaço e acento). O diretório atual do usuário não é a
  pasta da skill.
- Python: tente `python3`. No Windows use `python` (ou `py` se `python` não
  existir). Só precisa de Python 3.8+, sem instalar nada.
- Escreva o texto num arquivo `.txt` em UTF-8 numa pasta temporária e passe o
  caminho. Os scripts detectam português ou inglês sozinhos.

```bash
python3 "<pasta desta skill>/hookscore.py" ganchos.txt          # ranqueia as opções
python3 "<pasta desta skill>/hookscore.py" --hook "uma frase"   # nota de um gancho só
python3 "<pasta desta skill>/beats.py" roteiro.txt --target 30  # tempos antes de gravar
```

Se não tiver Python nenhum, siga o fluxo mesmo assim, avalie à mão pelos
mesmos critérios e **diga ao usuário** que a nota foi estimada, não calculada.

## Antes de escrever

1. Leia `~/.claude/instagram/voice.md` se existir. É o perfil de voz do
   usuário: como fala na câmera, o que nunca diz, com quem fala. Se não existir,
   peça **três reels ou legendas dele**, deduza a voz e escreva o arquivo (ou
   sugira rodar `/ig-voz`). Roteiro na voz errada não serve, porque ele vai ter
   que falar aquilo em voz alta.
2. Leia `hooks.json` nesta pasta. 26 fórmulas, cada uma com modelo, exemplo,
   versão de tela, pra que serve e como costuma ser estragada.
3. Se a ideia estiver fraca, não encha linguiça. Faça uma pergunta só, juntando
   tudo: o que aconteceu, com quem, e quanto custou ou rendeu. Um Reel precisa
   de uma coisa específica e verdadeira. Consiga isso antes de escrever.
4. Se `~/.claude/instagram/swipe.md` existir, leia. O `/ig-viral` escreve esse
   arquivo, e ele é a evidência do próprio usuário sobre quais fórmulas estão
   funcionando no nicho dele agora. Vale mais que os padrões daqui.

## O formato

Um Reel se decide nos dois primeiros segundos e se segura nos cinco seguintes.

```
0:00 - 0:02   GANCHO      a afirmação. Frase falada e frase de tela, escritas
                          separadas. Movimento no primeiro quadro, não rosto parado.
0:02 - 0:07   O QUE ESTÁ  por que isso importa pra quem está assistindo. Uma linha.
              EM JOGO
0:07 - ...    O CORPO     uma ideia por trecho, e o quadro muda a cada trecho.
ÚLTIMOS 3s    A ENTREGA   entregue o que o gancho prometeu, depois o único pedido.
ÚLTIMA LINHA  O LOOP      repita uma palavra do gancho pra o replay emendar liso.
```

Duração: 15 a 45 segundos é a faixa que funciona. Reels vão até 3 minutos e
quase ninguém deveria usar. Abaixo de 7 segundos o loop infla e nada mais.

## O fluxo

**1. Três ganchos, não um.** Passe a ideia pelo `hooks.json`, escolha três
fórmulas que realmente encaixam e escreva a frase falada e a frase de tela de
cada uma. Fórmulas diferentes, não três versões da mesma.

**2. Dê nota.** Ponha as três frases faladas num arquivo, uma por linha, e rode
`hookscore.py`. Mostre o ranking. Se o primeiro está abaixo de 50, você ainda
não tem o gancho e nenhuma edição resolve isso.

**3. Escreva o roteiro** em cima do gancho vencedor. Português falado, do jeito
que o usuário fala de verdade: "pra", "tá", "a gente". Frases curtas. Nenhuma
frase que ele precisaria ensaiar.

**4. Cronometre.** Rode `beats.py roteiro.txt --target {duração}`. Corrija cada
alerta: gancho passando de 3 segundos, trecho acima de 4 segundos, sequência de
trechos sem nada concreto, sem loop. Rode de novo até ficar limpo.

**5. Humanize.** Passe o roteiro pelo `/ig-human` antes de mostrar. Frase com
cara de texto escrito aparece na hora que alguém fala em voz alta.

**6. Entregue o bloco.** O roteiro num bloco de código, o texto da tela numa
lista separada com tempos, e depois:

```
REEL PRONTO
gancho:     #3 Ninguém Te Conta, nota 81 FORTE
duração:    28,4s em 9 trechos a 165 ppm
na tela:    6 cartelas
humanizador: 4 marcas tiradas, nota humana 81 PASSOU
legenda:    rode /ig-caption em seguida

Responda "sim" pra registrar, ou me diga o que mudar.
```

**7. Nunca publique.** Esta skill produz um roteiro. O usuário grava e posta.
No "sim", acrescente em `~/.claude/instagram/log.md` a data, a fórmula usada e
a primeira frase, pra o `/ig-audit` ter histórico depois.

## O texto da tela é outro roteiro

Escreva separado, sempre. Ele é lido antes de ser ouvido.

- **Seis palavras ou menos por cartela.** É lido de longe por alguém que ainda
  não está ouvindo.
- **A cartela do gancho aparece no quadro 1**, não depois de um silêncio.
- **Fique dentro da área segura.** Num quadro de 1080x1920, nada acima de y=230
  nem abaixo de y=1440, e deixe livres os 230 pixels da direita. A interface
  fica por cima de tudo fora dessa caixa: legenda, botões, faixa de áudio.
- **Nunca ponha o gancho onde fica a legenda.** É a parte de baixo e fica coberta.
- **Legende o corpo do vídeo.** A maioria assiste sem som primeiro.

## Regras que fazem a diferença

- **Uma ideia por Reel.** Se o roteiro tem duas, são dois Reels. Diga isso.
- **Número em vez de adjetivo.** "R$ 4.200" ganha de "muito dinheiro". Se o
  usuário não deu o número, pergunte em vez de escrever em volta do buraco.
- **Corte a introdução.** Sem "oi gente", sem "nesse vídeo", sem nome, sem
  vinheta. O vídeo começa na frase que você chegaria no segundo seis.
- **Mude o quadro a cada trecho.** Plano parado por 8 segundos é onde a pessoa
  sai, e o `beats.py` aponta isso.
- **Um pedido no final.** Comentar uma palavra, salvar ou seguir. Um.
- **Nunca invente.** Nada de métrica, cliente, faturamento ou resultado
  inventado no nome do usuário, nem como exemplo. Se precisa de um número e ele
  não deu, deixe `{{seu número}}` no roteiro e avise.
- **Não escreva roteiro em cima de áudio em alta que o usuário não pode usar.**
  Se a ideia precisa da voz dele, diga.

## Exemplo

```
/ig-reel a gente reduziu o tempo de proposta de 5 horas pra 20 minutos com um modelo
```

```
GANCHOS  (com nota)
  86  FORTE  #5  Tempo Encolhido     "Proposta me levava cinco horas. Hoje leva vinte minutos."
                                     na tela: 5 HORAS -> 20 MIN
  71  FORTE  #1  Confissão de Custo  "Eu cobrava quatro horas por semana só pra formatar. Por dois anos."
                                     na tela: 2 ANOS JOGADOS FORA
  54  OK     #9  Rouba Isso          "Rouba o modelo de proposta que fez isso."
                                     na tela: ROUBA ISSO

Vou com o #5: a proporção é crível, lê de uma vez na tela, e o número é seu.
```
