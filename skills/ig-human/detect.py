#!/usr/bin/env python3
"""
detect.py - painel de cinco checagens que dá nota pra quanto um texto parece
escrito por máquina. Funciona em português e em inglês (detecta sozinho).

O que isto é:  cinco heurísticas locais, inspiradas nos sinais que detectores
públicos de IA medem: variação no tamanho das frases, concretude, vocabulário
pronto, marcas tipográficas e voz. Tudo calculado na sua máquina. Nada é enviado.

O que isto NÃO é:  GPTZero, Originality, Copyleaks, Winston ou Turnitin. Não
chama nenhuma API e não promete o veredito deles. Pega as coisas que todos eles
olham, e por isso consertar tende a mexer nos números deles também. Essa é a
única promessa honesta.

Cada checagem dá uma nota HUMANA de 0 a 100. Maior é melhor.

Uso (no Windows troque python3 por python ou py)
  python3 detect.py rascunho.txt
  python3 detect.py rascunho.txt --json
  python3 detect.py antes.txt depois.txt      # compara dois textos
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")
sys.path.insert(0, HERE)
from langdetect_ig import detect_lang, entries_for, utf8_console  # noqa: E402

utf8_console()

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")
NUMBERS = re.compile(r"(?:R\$|US\$|\$|€)\s?\d[\d,.]*|\b\d[\d,.]*%?")
# Número falado também é concreto: "nove dias", "duas vezes", "three years".
SPOKEN = re.compile(
    r"\b(?:dois|duas|três|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|quinze|vinte|trinta|"
    r"quarenta|cinquenta|cem|mil|milhão|milhões|metade|dobro|two|three|four|five|six|seven|"
    r"eight|nine|ten|twelve|twenty|thirty|fifty|hundred|thousand|million|half|twice)\b",
    re.IGNORECASE)
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}\b", re.MULTILINE)

# "Contrações" = marcas de fala natural. Em inglês: don't, it's. Em português:
# pra, tá, né, a gente, cê. Texto de IA quase nunca usa nenhuma das duas.
CASUAL = {
    "en": re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(?:pra|pro|pros|pras|tá|tô|tava|tamo|né|cê|vc|vcs|a gente|num|numa|"
                     r"dum|duma|bora|vamo|tipo|aí|daí|pq|tbm|também não|sei lá|beleza)\b",
                     re.IGNORECASE),
}
PRONOUNS = {
    "en": re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(eu|me|mim|meu|minha|meus|minhas|nós|a gente|nosso|nossa|você|vocês|"
                     r"voce|vc|te|seu|sua|seus|suas|teu|tua)\b", re.IGNORECASE),
}
# Português escrito usa menos contração que inglês, então a régua é mais baixa.
CASUAL_HUMAN = {"en": 3.0, "pt": 1.5}

NAMES = {"BURSTINESS": "VARIAÇÃO", "SPECIFICITY": "CONCRETUDE", "SLOP DENSITY": "VOCAB. IA",
         "FINGERPRINT": "DIGITAL", "VOICE": "VOZ"}
VERDICTS = {"PASS": "PASSOU", "REVIEW": "REVISAR", "FLAGGED": "CARA DE IA"}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text, lex, lang):
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "curto demais pra julgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    return scale(cv, human=0.70, machine=0.22), \
        f"variação {cv:.2f} em {len(lens)} frases (ideal 0,55+)"


def check_specificity(text, lex, lang):
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais pra julgar"
    hits = (len(NUMBERS.findall(text)) + len(SPOKEN.findall(text))
            + len(set(PROPER.findall(text))))
    density = hits * 100 / len(w)
    return scale(density, human=6.0, machine=0.5), \
        f"{hits} marcadores concretos, {density:.1f} a cada 100 palavras (ideal 4+)"


def check_slop(text, lex, lang):
    w = words(text)
    if not w:
        return 50.0, "vazio"
    hits, found = 0, []
    for entry in entries_for(lex, "words", lang) + entries_for(lex, "phrases", lang):
        pattern = re.compile(r"(?<!\w)" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"(?!\w)",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    detail = f"{hits} termos prontos, {density:.1f} a cada 100 palavras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return scale(density, human=0.0, machine=4.0), detail


def check_fingerprint(text, lex, lang):
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf" and c != "‍")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    return scale(per1k, human=0.0, machine=12.0), \
        (f"{invisible} invisível, {em} travessão, {curly} aspas curvas, "
         f"{ellip} reticências, {nbsp} espaço duro")


def check_voice(text, lex, lang):
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais pra julgar"
    per100 = 100 / len(w)
    casual = len(CASUAL[lang].findall(text)) * per100
    person = len(PRONOUNS[lang].findall(text)) * per100
    tells, names = 0, []
    for s in entries_for(lex, "structures", lang):
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(casual, human=CASUAL_HUMAN[lang], machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("bullets-iguais")
    label = "marcas de fala" if lang == "pt" else "contrações"
    detail = (f"{casual:.1f} {label}, {person:.1f} pronomes pessoais a cada 100 palavras, "
              f"{tells} padrão(ões) de estrutura")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]
FUNCS = {"BURSTINESS": check_burstiness, "SPECIFICITY": check_specificity,
         "SLOP DENSITY": check_slop, "FINGERPRINT": check_fingerprint, "VOICE": check_voice}


def run(text, lex, lang="auto"):
    lang = detect_lang(text) if lang == "auto" else lang
    results = {c: FUNCS[c](text, lex, lang) for c in CHECKS}
    scores = [results[c][0] for c in CHECKS]
    # A checagem mais fraca pesa: detector só precisa de um sinal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict, lang


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, lang, label=None, out=sys.stdout):
    title = f"PAINEL DE DETECÇÃO DE IA  (idioma: {lang})" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {NAMES[name]:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {overall:5.1f}   {VERDICTS[verdict]}", file=out)
    if verdict != "PASS":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sinal mais fraco: {NAMES[weakest]}. Conserte esse primeiro.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota pra quanto um texto parece escrito por máquina.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - pra ler da entrada")
    ap.add_argument("compare", nargs="?", help="segundo arquivo, pra comparar antes/depois")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto")
    args = ap.parse_args()

    with open(args.lexicon, encoding="utf-8") as fh:
        lex = json.load(fh)

    def read(p):
        if p == "-":
            return sys.stdin.read()
        with open(p, encoding="utf-8-sig") as fh:
            return fh.read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))
    # Mesmo idioma nos dois lados da comparação, decidido pelo primeiro texto.
    lang = args.lang if args.lang != "auto" else detect_lang(targets[0][1])

    payload, runs = [], []
    for name, text in targets:
        results, overall, verdict, _ = run(text, lex, lang)
        runs.append((results, overall, verdict))
        payload.append({
            "source": name,
            "lang": lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, _), (results, overall, verdict) in zip(targets, runs):
        render(results, overall, verdict, lang,
               label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {VERDICTS[a['verdict']]}  ->  "
              f"{b['human_score']:.1f} {VERDICTS[b['verdict']]}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
