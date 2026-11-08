---
name: ig-plan
description: >-
  Monta a semana no Instagram: o que postar, em qual formato, quando, e com
  quem engajar. Use quando o usuário disser "planeja minha semana", "o que eu
  posto", "calendário de conteúdo", "não sei sobre o que postar", ou quiser
  uma agenda de posts e uma lista de engajamento.
---

# ig-plan

A sala de controle. Todo o resto do pacote executa; esta decide o que vai ser
executado. Rode uma vez por semana, sempre no mesmo dia.

## Entrada

Se `~/.claude/instagram/voice.md`, `swipe.md` e `log.md` existirem, leia. O
swipe file é a evidência do próprio usuário (do `/ig-viral`) sobre quais
fórmulas estão funcionando no nicho dele agora, e vale mais que qualquer coisa
deste arquivo. O log evita o plano repetir um tema das últimas duas semanas.

Se não existirem, peça quatro coisas e anote:

1. O que o usuário vende, e pra quem.
2. Os três ou quatro temas pelos quais ele quer ser conhecido.
3. O que aconteceu de verdade essa semana: uma call com cliente, um número, um
   erro, algo que ele construiu, uma discussão. É daqui que os posts saem.
4. Dez contas pra quem vale a pena aparecer.

## O que postar

Quatro a cinco posts por semana, pelo menos três Reels. Reels são o único
formato do Instagram que alcança com consistência quem não segue a conta.
Carrossel aprofunda com quem já segue. Stories são diários e planejados à parte.

Misture na semana, nunca dois do mesmo tipo seguidos:

| tipo | frequência | função |
| --- | --- | --- |
| **Prova** | 1 por semana | algo que aconteceu, com número. Reel. |
| **Ensino** | 1 a 2 por semana | uma coisa que a pessoa consegue fazer hoje. Reel ou carrossel. |
| **Opinião** | 1 por semana | uma posição que pode te fazer perder seguidor. Reel. |
| **História** | 1 a cada 2 semanas | uma cena com um custo. Reel. |
| **Oferta** | 1 a cada 2 semanas | o que você vende, dito com clareza, sem pedir desculpa. Carrossel ou stories. |

Pra cada slot dê: o tema, o ângulo específico a partir do que aconteceu de
verdade na semana, o formato e o número da fórmula de gancho do
`ig-reel/hooks.json`. Não um assunto, um ângulo. "IA" não é plano. "A proposta
que a gente perdeu porque o rascunho tinha um travessão" é um Reel.

## Quando postar

Poste quando o público do usuário está acordado e fora do trabalho. Pra
público geral costuma ser começo da noite, no horário local; pra público de
negócios, começo da manhã.

Mas diga com clareza: **o horário importa muito menos que os dois primeiros
segundos.** O Instagram continua mostrando um Reel por dias se ele performa, e
enterra um bem postado que não performa. Se o usuário está otimizando horário
antes do gancho funcionar, está polindo a coisa errada, e você deve dizer isso.

Use o fuso do público, não o do usuário, se forem diferentes.

## A rodada de engajamento, que não é opcional

20 minutos por dia, antes de postar, não depois. Monte uma lista de 10:

- **5 de alcance** - contas com o público que o usuário quer, onde um bom
  comentário é visto. Comente cedo, antes da conversa ter 200 comentários.
- **3 pares** - mesmo tamanho, mesma área. É o grupo que retribui.
- **2 compradores** - gente que poderia comprar de verdade. Comente por semanas
  antes de qualquer DM, e nunca venda em comentário.

Passe a lista pro `/ig-comment`.

## Saída

```
SEMANA DE 15/SET

SEG  só engajamento  (20 min, lista abaixo)
TER  19h30  REEL       PROVA    #5  Tempo Encolhido  - proposta de 5h pra 20 min
QUA  só stories + engajamento
QUI  19h00  CARROSSEL  ENSINO   legenda Trabalho B   - a cláusula em 4 slides
SEX  19h30  REEL       OPINIÃO  #2  Ordem Negativa   - para de fazer call de descoberta
SÁB  -
DOM  18h00  REEL       HISTÓRIA #21 Começo No Meio   - o e-mail de reembolso

STORIES  todo dia, 3 a 5 telas, caixa de pergunta na quinta.

ENGAJAR  (5 alcance / 3 pares / 2 compradores)
  ...

Diga "escreve a terça" que eu faço o rascunho.
```

Salve o plano em `~/.claude/instagram/plan.md` pra as outras skills lerem. Nada
é agendado nem postado em lugar nenhum. Isso é um plano e quem executa é o usuário.
