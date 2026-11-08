#!/usr/bin/env python3
"""
humanize.py - tira a "cara de IA" de um rascunho (português ou inglês).

Três passadas, nesta ordem:

  1. INVISÍVEIS  apaga ou normaliza caracteres que teclado humano não produz:
                 zero-width, word joiner, hífen suave, BOM, caracteres de tag
                 Unicode, espaços não separáveis. Eles sobrevivem ao copiar e
                 colar e são a marca mais mecânica de texto gerado.
  2. TIPOGRAFIA  travessão (—) vira vírgula, meia-risca vira hífen, aspas
                 curvas viram retas, reticências (…) viram três pontos.
  3. VOCABULÁRIO troca o vocabulário de IA do slop.json por palavras simples,
                 mantendo maiúsculas e sem mexer em links.

O idioma é detectado sozinho (ou force com --lang pt / --lang en) e só o bloco
daquele idioma do slop.json é aplicado.

Padrões de estrutura ("não é só X, é Y", tríades, parede de hashtag) são
APONTADOS, nunca reescritos sozinhos. Mudar o formato de uma frase pede
julgamento, então isso é trabalho do Claude, não de uma regex.

Uso (no Windows troque python3 por python ou py)
  python3 humanize.py rascunho.txt
  python3 humanize.py rascunho.txt --report
  python3 humanize.py rascunho.txt --json
  python3 humanize.py rascunho.txt -o limpo.txt --report
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")
sys.path.insert(0, HERE)
from langdetect_ig import detect_lang, entries_for, utf8_console  # noqa: E402

utf8_console()

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> int;  'U+E0000-U+E007F' -> (início, fim)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Troca links por marcadores pra nenhuma passada mexer dentro de um link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


EMOJI_ZWJ = re.compile(r"(?<=[\U0001F000-\U0001FAFF☀-➿️])‍"
                       r"(?=[\U0001F000-\U0001FAFF☀-➿])")


def pass_invisible(text, lex):
    hits = []
    # O zero-width joiner DENTRO de um emoji composto (👨‍👩‍👧, 🏃‍♀️) é legítimo:
    # apagar ele quebra o emoji em vários. Protege esse caso.
    text = EMOJI_ZWJ.sub("\x00ZWJ\x00", text)
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": "apagar" if entry["action"] == "delete" else "espaço"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Qualquer caractere de formatação (Cf) que sobrou é invisível por definição.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "outros caracteres invisíveis", "count": len(stray),
                     "action": "apagar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text.replace("\x00ZWJ\x00", "‍"), hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(espaço)"})
        if ch == "—":
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)
            text = re.sub(r"\s+–\s+", ", ", text)
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex, lang="en"):
    """Troca palavras e frases de IA. As mais longas primeiro, pra frase ganhar de palavra."""
    hits = []
    entries = sorted(entries_for(lex, "phrases", lang) + entries_for(lex, "words", lang),
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        rx = r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)"
        if entry["family"] in ("conectivos", "connectives"):
            rx += r"(?:\s*,)?"          # "Além disso, X" vira "E X", não "E, X"
        pattern = re.compile(rx, re.IGNORECASE)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(apagado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpeza depois de apagar: apagar uma oração inteira deixa pontuação órfã
    # ("sistema. ." ou uma linha que agora começa com vírgula).
    text = re.sub(r"[ \t]{2,}", " ", text)
    # conjunção que ficou sozinha antes da pontuação: "dicas e !" -> "dicas!"
    text = re.sub(r"(?i)[ \t]+(?:e|ou|and|or)[ \t]*([.!?])", r"\1", text)
    # pontuação órfã no começo da linha (mas "..." de propósito, tipo gancho #21, fica)
    text = re.sub(r"(?m)^[ \t]*(?:(?:[,;:!?]|\.(?!\.))+[ \t]*)+", "", text)
    text = re.sub(r"\.[ \t]*([!?])", ".", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = text.replace("...", "\x00ELL\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Travessão que virou vírgula + conectivo vira emenda ("é importante, também, é prova").
    text = re.sub(r"(?i),\s*(also|so|still|basically|in the end|também|então|ainda|no fim)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex, lang="en"):
    flags = []
    for s in entries_for(lex, "structures", lang):
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases todas do mesmo tamanho (variação {cv:.2f})",
                "count": len(lens),
                "fix": "Quebre uma frase no meio. Deixe outra correr longa. Máquina escreve tudo igual.",
            })
    return flags


def restore_capitals(original, text):
    """Apagar uma abertura deixa a próxima palavra em minúscula.

    Só corrige pra quem já escreve com maiúscula no começo da frase: uma voz
    toda em minúscula é estilo, não defeito.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([^\W\d_])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-zà-ÿ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex, lang="auto"):
    lang = detect_lang(text) if lang == "auto" else lang
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex, lang)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "lang": lang,
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex, lang),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head(f"RELATÓRIO DO HUMANIZADOR  (idioma: {report['lang']})")
    print(f"{total} marcas de máquina removidas, "
          f"{len(report['structures'])} padrão(ões) de estrutura pra reescrever", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISÍVEIS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. VOCABULÁRIO DE IA")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. PADRÕES DE ESTRUTURA  (não corrigidos sozinhos - reescreva)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report[k] for k in ("invisible", "typographic", "lexical", "structures")):
        head("LIMPO")
        print("  Nada pra tirar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Tira a cara de IA de um rascunho.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - pra ler da entrada")
    ap.add_argument("-o", "--out", help="salvar o texto limpo aqui em vez de imprimir")
    ap.add_argument("--report", action="store_true", help="mostrar o que mudou (no stderr)")
    ap.add_argument("--json", action="store_true", help="saída {text, report} em JSON")
    ap.add_argument("--lexicon", default=LEX, help="caminho do slop.json")
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, args.lang)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"salvo em {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
