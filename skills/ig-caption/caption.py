#!/usr/bin/env python3
"""
caption.py - revisa uma legenda de Instagram e mostra exatamente o que o feed
mostra antes do "... mais". Funciona com legenda em português ou inglês.

O Instagram mostra uns 125 caracteres da legenda no feed e esconde o resto
atrás de um toque. Quase toda legenda que falha, falha ali: o gancho está na
terceira frase, a primeira linha é um "oi gente", ou tudo começa com hashtag.
Isto imprime a janela visível numa caixa, do jeito que um desconhecido lê
rolando o feed, e depois checa as coisas que valem a pena checar.

O corte de 125 é aproximado: muda com o aparelho, o tamanho da fonte e onde
caem suas quebras de linha. Por isso deixe folga. Mude com --truncate.

Uso (no Windows troque python3 por python ou py)
  python3 caption.py legenda.txt
  python3 caption.py legenda.txt --keywords "edição de vídeo,contrato freelancer"
  python3 caption.py legenda.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

LIMIT = 2200             # limite rígido de legenda do Instagram.
TRUNCATE = 125           # mais ou menos onde o feed corta pro "... mais".
HASHTAG_LIMIT = 5        # limite por post/reel desde 18/12/2025 (antes era 30),
                         # segundo o anúncio da conta @Creators. Regras de
                         # plataforma mudam: se o Instagram mudar de novo, mude aqui.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|com\.br|br|co|io|net|org|ai|app)(?:/\S*)?\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿]")
CONCRETE_RE = re.compile(r"(?:R\$|US\$|\$|€)\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}\b",
                         re.MULTILINE)

ASKS = [
    # português
    (re.compile(r"(?i)\bcomenta(?:r|e)?\s+(?:a palavra\s+|aqui\s+)?[\"“']?[A-ZÁÉÍÓÚÃÕÇ0-9]{2,}\b"), "comentar uma palavra-chave"),
    (re.compile(r"(?i)\b(?:me chama|me manda|manda)\s+(?:uma\s+)?(?:dm|direct|mensagem|msg)\b|\bchama no direct\b"), "chamar na DM"),
    (re.compile(r"(?i)\bsalv[ae]\s+(?:esse|este|isso|o post|pra)\b"), "salvar"),
    (re.compile(r"(?i)\b(?:compartilh[ae]|mand[ae])\s+(?:esse|este|isso|pra|para)\b"), "compartilhar/mandar"),
    (re.compile(r"(?i)\b(?:me segue|siga|segue o perfil|segue a gente)\b"), "seguir"),
    (re.compile(r"(?i)\blink na bio\b"), "link na bio"),
    (re.compile(r"(?i)\b(?:arrasta|desliza|passa) (?:pro lado|pra lado|para o lado)\b"), "arrastar"),
    (re.compile(r"(?i)\bme (?:conta|diz|fala)\b|\bqual (?:você|vc) (?:prefere|escolhe)\b"), "responder uma pergunta"),
    # inglês
    (re.compile(r"(?i)\bcomment (?:the word |\")?[A-Z0-9]{2,}\b"), "comment a keyword"),
    (re.compile(r"(?i)\b(?:dm|message) me\b"), "DM me"),
    (re.compile(r"(?i)\bsave (?:this|it)\b"), "save this"),
    (re.compile(r"(?i)\bshare (?:this|it)\b"), "share this"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b"), "follow"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b"), "link in bio"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b"), "answer a question"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily", "#paravoce", "#paravocê",
               "#viralizar", "#viraliza", "#explorar", "#reelsbrasil", "#brasil", "#sigam",
               "#seguidores", "#curtidas", "#likes", "#tbt", "#instagram", "#insta", "#foto",
               "#sucesso", "#motivação", "#motivacao"}

ORDER = {"FAIL": "FALHA", "WARN": "ATENÇÃO", "PASS": "OK"}
VERDICT = {"FIX": "CONSERTAR", "REVIEW": "REVISAR", "READY": "PRONTA"}


def visible_window(text, cut):
    """O que o feed mostra. O Instagram corta no meio da palavra, então aqui também."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  O QUE O FEED MOSTRA", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... mais" if truncated else "(cabe inteira)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = stripped.split("\n")
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = sorted({name for pattern, name in ASKS if pattern.search(stripped)})
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("TAMANHO", "FAIL" if chars > LIMIT else "PASS",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} acima do limite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMEIRA LINHA", "FAIL", "a legenda começa com uma linha em branco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMEIRA LINHA", "FAIL",
            "começa com hashtag ou menção, na única posição que vale uma frase")
    elif re.match(r"(?i)^\s*(?:oi\b|olá|ola\b|e a[ií]\b|fala (?:galera|pessoal|gente)|bom dia|boa tarde|boa noite|hey\b|hi\b)", first_line):
        add("PRIMEIRA LINHA", "WARN", "começa com cumprimento, gastando a janela visível com nada")
    elif len(first_line) > cut:
        add("PRIMEIRA LINHA", "WARN",
            f"{len(first_line)} caracteres, então é cortada em {cut} no meio do pensamento. "
            "Tudo bem se o corte for um suspense, ruim se for no meio de uma oração")
    else:
        add("PRIMEIRA LINHA", "PASS", f"{len(first_line)} caracteres, aparece inteira")

    n_conc = len(CONCRETE_RE.findall(window))
    add("GANCHO CONCRETO", "PASS" if n_conc else "WARN",
        f"{n_conc} número(s) ou nome(s) na parte visível"
        + ("" if n_conc else " - nada checável antes do toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FAIL", f"{len(tags)} hashtags, acima do limite de {HASHTAG_LIMIT} do Instagram. "
                                "As que passam da quinta não contam e o bloco parece velho")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} hashtags, {len(filler)} genérica(s) "
                                f"({', '.join(filler[:3])}). Essas não descrevem nada")
    else:
        add("HASHTAGS", "PASS", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("LUGAR DAS TAGS", "PASS", "sem hashtags")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?!\w)", window) for t in tags):
        add("LUGAR DAS TAGS", "WARN", "tem hashtag dentro da parte visível, "
                                      "gastando espaço do feed com etiqueta")
    else:
        add("LUGAR DAS TAGS", "PASS", "hashtags abaixo da dobra")

    add("LINKS", "WARN" if links else "PASS",
        f"{len(links)} link(s) na legenda, e link em legenda não é clicável. "
        "Ponha na bio ou mande na DM" if links else "nenhum link morto no texto")

    if len(asks) == 1:
        add("UM PEDIDO SÓ", "PASS", f"uma chamada pra ação: {asks[0]}")
    elif not asks:
        add("UM PEDIDO SÓ", "WARN", "nenhuma chamada pra ação. Decida pra que serve esse post")
    else:
        add("UM PEDIDO SÓ", "WARN", f"{len(asks)} pedidos ({', '.join(asks)}). "
                                    "Dois pedidos é o mesmo que nenhum")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 4 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} a cada 100 caracteres"
        + (" - vira enfeite" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("TERMOS DE BUSCA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} na parte visível" if found else "")
            + (f". Faltando: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "FIX" if fails else ("REVIEW" if warns else "READY")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISÃO DA LEGENDA  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {ORDER[c['status']]:<8} {c['check']:<17} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDITO  {VERDICT[a['verdict']]}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa uma legenda de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo da legenda, ou - pra ler da entrada")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres mostrados antes do '... mais' (padrão {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="termos pelos quais você quer ser achado, separados por vírgula")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "READY" else 1)


if __name__ == "__main__":
    main()
