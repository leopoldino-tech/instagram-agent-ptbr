#!/usr/bin/env python3
"""
beats.py - transforma o roteiro de um Reel numa planilha de tempos (beat sheet)
antes de você gravar. Funciona com roteiro em português ou inglês.

Estima quanto tempo cada linha leva pra ser falada, empilha em timecodes e
aponta as quatro coisas que matam um Reel na edição: gancho que passa de três
segundos, um trecho tão longo que a pessoa sai, uma sequência de linhas sem
nada concreto, e um tamanho total que não bate com o que você queria.

Os tempos são uma estimativa pela contagem de palavras numa velocidade de fala.
Servem pra planejar a edição, não substituem gravar. Ajuste com --wpm depois de
cronometrar você lendo um roteiro em voz alta: a maioria fica entre 150 e 200
palavras por minuto. O padrão é 165.

Uso (no Windows troque python3 por python ou py)
  python3 beats.py roteiro.txt
  python3 beats.py roteiro.txt --target 30
  python3 beats.py roteiro.txt --wpm 185 --target 45
  python3 beats.py roteiro.txt --json
"""

import argparse
import json
import re
import sys
import unicodedata

for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORD_RE = re.compile(r"[\w$%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(
    r"(?:R\$|US\$|\$|€)\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}\b"
    r"|\b(?:dois|duas|três|quatro|cinco|seis|sete|oito|nove|dez|vinte|trinta|cem|mil|milhão|"
    r"two|three|four|five|six|seven|eight|nine|ten|twenty|hundred|thousand|million)\b",
    re.MULTILINE | re.IGNORECASE)


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


STOPWORDS = {fold(w) for w in (
    "the a an and or but if of to in on for with that this it is are was were be been you your "
    "i my me we our they them he she so just not no do did does have has had will can at as by "
    "from out up off one all "
    # português
    "o a os as um uma uns umas e ou mas se de do da dos das no na nos nas em por pra pro para "
    "com que é foi era ser ter tem tinha você voce vc seu sua eu meu minha me te a gente nós "
    "eles elas ele ela isso esse essa este esta aquilo só não nao sim já mais muito também "
    "como quando onde aí ai lá la aqui vai vou tá ta né"
).split()}

HOOK_WINDOW = 3.0        # segundos. Depois disso o dedo já decidiu.
MAX_BEAT = 4.0           # segundos numa ideia só sem mudar nada na tela.
ABSTRACT_RUN = 3         # trechos seguidos sem nada checável.


def words(text):
    # "R$ 18.000" é uma palavra só quando falado.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Uma linha é um trecho, a não ser que a linha seja longa demais pra ser um só."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1, "start": round(clock, 2), "dur": round(dur, 2), "words": n,
            "text": text, "concrete": len(CONCRETE_RE.findall(text)), "label": "", "flags": [],
        })
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MEIO"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"gancho leva {rows[0]['dur']:.1f}s, passa dos {HOOK_WINDOW:.0f}s")
        notes.append(f"O trecho 1 leva {rows[0]['dur']:.1f}s pra ser falado. Corte pra "
                     f"{int(HOOK_WINDOW * wps)} palavras ou menos, senão o gancho chega depois "
                     "que a pessoa já decidiu.")
    if rows[0]["concrete"] == 0:
        notes.append("O trecho 1 não tem número nem nome. Gancho sem nada checável é o que "
                     "a pessoa passa reto.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s num trecho só")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Trecho(s) {', '.join(map(str, long_beats))} passam de {MAX_BEAT:.0f}s. "
                     "Quebre a linha ou mude o que aparece na tela no meio dela. "
                     "Quadro parado é onde a pessoa sai.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Trechos {start}-{r['n']} não têm nada concreto. "
                             "Ponha um número, um nome ou um preço em um deles.")
        else:
            run, start = 0, None

    first = {fold(w) for w in words(rows[0]["text"]) if fold(w) not in STOPWORDS}
    last = {fold(w) for w in words(rows[-1]["text"]) if fold(w) not in STOPWORDS}
    loop = sorted(first & last)
    if loop:
        notes.append(f"Fecha o loop: o último trecho repete \"{', '.join(loop[:3])}\" do gancho. "
                     "Segunda visualização é alcance de graça.")
    else:
        notes.append("Sem loop. O último trecho não repete nenhuma palavra do gancho, então o "
                     "vídeo termina seco. Repetir uma palavra do trecho 1 é o replay mais barato que existe.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Tamanho no alvo ({total:.1f}s contra {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s acima do alvo. Corte umas {int(delta * wps)} palavras.")
        else:
            notes.append(f"{-delta:.1f}s abaixo do alvo. Acrescente {int(-delta * wps)} palavras "
                         "ou grave curto mesmo. Curto quase sempre é melhor.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows, "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"PLANILHA DE TEMPOS  ·  {a['total_words']} palavras  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['wpm']:g} ppm" + (f"  ·  alvo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Cronometra um roteiro de Reel.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo do roteiro, ou -")
    ap.add_argument("--wpm", type=float, default=165, help="palavras por minuto (padrão 165)")
    ap.add_argument("--target", type=float, help="duração alvo em segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("roteiro vazio", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
