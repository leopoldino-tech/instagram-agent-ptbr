---
name: ig-voz
description: >-
  Primeiro passo do pacote de Instagram: cria ou atualiza o perfil de voz do
  usuário em ~/.claude/instagram/voice.md, que todas as outras skills ig-* leem.
  Use quando o usuário disser "configura minha voz", "cria meu voice.md",
  "aprende meu jeito de falar", "começar", "primeiros passos", mandar reels ou
  legendas dele pra o Claude aprender o estilo, ou quando outra skill ig-* não
  encontrar o voice.md.
---

# ig-voz

Todo o pacote depende de uma coisa: escrever do jeito que o usuário **fala**,
porque ele vai ter que dizer aquilo na câmera. Esta skill monta esse perfil uma
vez, e todas as outras leem.

## Onde fica

`~/.claude/instagram/voice.md` (no Windows: `C:\Users\<usuário>\.claude\instagram\voice.md`).
Crie a pasta `~/.claude/instagram/` se não existir. O modelo do arquivo está em
`voice-modelo.md`, na mesma pasta deste SKILL.md.

Se o arquivo já existir, leia, mostre um resumo de três linhas e pergunte o que
mudar. Não sobrescreva sem perguntar.

## Fluxo

**1. Peça material real, não respostas.** Numa mensagem só:

- três reels (transcrição, link que você consiga abrir, ou o texto falado) ou
  três legendas que o usuário acha que "mais parecem ele";
- o @ e, em uma frase, o que ele faz e pra quem;
- se ele tem números ou resultados reais que topa usar em público.

Se ele só mandar o @, não invente a partir do nome. Peça os textos.

**2. Deduza a voz do material.** Anote o que você observou de verdade, com
exemplos tirados dos textos dele:

- tamanho típico de frase, se fala rápido ou devagar;
- marcas de fala ("pra", "tá", "né", "mano", "gente", gírias regionais);
- se usa palavrão, emoji, caixa alta;
- palavras que ele repete; palavras de "IA" que ele nunca usaria;
- como ele abre e fecha os vídeos;
- opiniões fortes que aparecem nos textos.

**3. Faça só as perguntas que o material não respondeu.** No máximo cinco,
numa mensagem: posições polêmicas dele, o que está fora dos limites, a
palavra-chave de CTA, pra onde vai o link.

**4. Escreva o arquivo** seguindo o `voice-modelo.md`, preenchido com o que
você observou e o que ele respondeu. Onde não souber, deixe o campo em branco.
**Nunca invente prova, número ou cliente.**

**5. Mostre e confirme.** Mostre o arquivo e pergunte "tá parecido com você?".
Ajuste o que ele corrigir. Só então salve.

**6. Próximo passo.** Diga em uma linha o que ele pode fazer agora:

```
VOZ SALVA em ~/.claude/instagram/voice.md

Próximos passos:
  /ig-profile   nota do seu perfil e o que corrigir primeiro
  /ig-reel      transforma uma ideia num roteiro de Reel
  /ig-plan      monta sua semana
```

## Regras

- O arquivo é do usuário. Escreva em português simples, sem jargão.
- Não copie frases inteiras de outros criadores pra dentro do perfil de voz.
- Se o usuário pedir pra "falar igual" a algum criador famoso, explique que o
  pacote escreve na voz **dele**; dá pra pegar formato e ritmo, não a identidade de outra pessoa.
