---
name: ig-comment
description: >-
  Escreve comentários em posts e reels de outras pessoas que soam como alguém
  com opinião, não como robô. Use quando o usuário colar um post ou reel e
  quiser um comentário, disser "comenta nisso", "engaja aqui", "o que eu falo
  aqui", ou quiser um lote pra rodada diária de engajamento.
---

# ig-comment

Comentar são os vinte minutos de maior alavanca no Instagram, e os mais fáceis
de fazer mal. Um comentário no topo de um reel com 40 mil views é visto por
mais gente que a maioria dos posts da própria conta, e é o único lugar onde um
desconhecido toca direto num perfil.

Comentário genérico é pior que nenhum. Gasta um toque que não leva a lugar
nenhum e marca a conta como "conta de grupo de engajamento" pra única pessoa
cuja opinião importava: o criador.

## Entrada

O usuário cola o texto do post ou reel, ou um print, com o nome da conta. Se
ele mandar um link que você não consegue abrir, peça pra colar. Não use
navegador pra raspar o feed e não poste nada.

## Os nove tipos de comentário

Escolha pelo que o post realmente é. Nunca vá no tipo 1 por padrão.

| # | tipo | quando | formato |
| --- | --- | --- | --- |
| 1 | **Acrescentar um dado** | o post afirma algo que você sustenta com número | "Aqui foi igual: 40% de..." |
| 2 | **O caso que faltou** | o post está certo mas incompleto | "Isso vale até {condição}." |
| 3 | **Discordar com respeito** | você acha mesmo que está errado | diga onde concorda primeiro, depois a divergência |
| 4 | **Puxar uma linha** | uma frase do post é a boa | cite ela, construa em cima |
| 5 | **A pergunta de verdade** | o post pulou a parte difícil | uma pergunta, específica |
| 6 | **O comprovante** | você já fez o que ele descreveu | o que aconteceu, duas frases |
| 7 | **A correção** | tem um erro factual | esteja certo, seja breve, gentil e seguro |
| 8 | **Outro ângulo** | fatos certos, leitura errada | "Outro jeito de ler isso:" |
| 9 | **A frase curta** | o post não precisa de nada, você quer presença | menos de 10 palavras, engraçada ou verdadeira |

## Regras

- **Uma a três frases.** Comentário é lido numa coluna estreita embaixo de um
  vídeo. Parágrafo vira "ver mais" e ninguém toca.
- **Nunca comece com** "Ótimo post", "Amei", "Verdade", "Isso 👏", "Precisava
  ouvir isso hoje", ou o nome do criador com exclamação. Tudo isso é invisível.
- **Nada de comentário só com emoji** e nada de emoji como primeiro caractere.
- **Nunca repita o reel.** Todo mundo que está lendo acabou de assistir.
- **Uma ideia.** Comentário com dois pontos parece sequestro do post.
- **Diga a coisa específica.** Se o comentário serviria embaixo de qualquer
  post do assunto, não é comentário, é ruído.
- **Nunca venda, jamais.** Nem a oferta, nem o link, nem "dá uma olhada no meu
  perfil". É o jeito mais rápido de ser bloqueado justo por quem você queria alcançar.
- **Cedo importa mais aqui que em qualquer lugar.** Comentário na primeira hora
  de um reel que depois viaja vai junto com ele.

## Saída

Dê **duas opções de tipos diferentes**, com rótulo, e uma linha dizendo qual
você postaria e por quê. Passe as duas pelo `/ig-human` antes: comentário é
curto, então um travessão ou uma frase pronta grita mais aqui que numa legenda.

```
OPÇÕES DE COMENTÁRIO  (no reel do @conta sobre preço)

[6 · Comprovante]
A gente subiu 40% em março passado e perdeu um cliente só, justo o que ocupava
metade da caixa de entrada. Levei oito meses pra parar de ter medo disso.

[3 · Discordar com respeito]
Concordo com a ancoragem. O que eu questionaria é fazer isso no meio do
projeto. Tentei e custou uma renovação que estava tranquila.

Posta o primeiro. Ele cede em algo e tem um número.
```

## Modo lote

Pra rodada de engajamento, peça os 5 a 10 posts como texto colado numa
mensagem só, devolva um comentário pra cada num bloco único, e mantenha uma
anotação em `~/.claude/instagram/log.md` de quem já recebeu comentário essa
semana. Comentar nas mesmas três contas todo dia aparece, e parece exatamente
o que é.

## Nunca

Não poste sozinho, não automatize comentário e não use navegador pra publicar
no lugar do usuário. Engajamento automatizado viola os Termos de Uso do
Instagram e bloqueia contas. Esta skill escreve o comentário. O usuário posta.
