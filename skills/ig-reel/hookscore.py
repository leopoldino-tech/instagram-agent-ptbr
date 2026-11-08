#!/usr/bin/env python3
"""
hookscore.py - dá nota para a primeira frase de um Reel (o gancho) em cinco
propriedades que ganchos fortes têm em comum, e ranqueia vários ganchos.

Funciona em português do Brasil e em inglês. O idioma é detectado sozinho
(ou force com --lang pt / --lang en).

O que isto é:  cinco heurísticas locais, calculadas na sua máquina só a partir
do texto. Medem coisas que ganchos que seguram atenção costumam ter: dá pra
falar em menos de três segundos, tem algo concreto, tem algo em jogo, a parte
interessante vem no começo e fala com alguém.

O que isto NÃO é:  um previsor de views. O autor original testou em 74 ganchos
reais (em inglês): separa gancho ruim de gancho real muito bem (AUC 0,83), mas
quase não separa o hit do flop do mesmo criador (AUC 0,56, onde 0,50 é cara ou
coroa). Use pra matar ganchos fracos antes de gravar. Quem decide qual de dois
ganchos bons vai rodar é o gráfico de retenção, não um script.

Cada checagem vai de 0 a 100. Maior é melhor.

Uso (no Windows troque python3 por python ou py)
  python3 hookscore.py ganchos.txt              # um gancho por linha, ranqueados
  python3 hookscore.py --hook "Perdi R$ 18 mil por causa de um contrato."
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

# Windows: o console padrão (cp1252) quebra com emoji e acentos. Força UTF-8.
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORD_RE = re.compile(r"[\w$%'’-]+")
NUMBER_RE = re.compile(
    r"(?:R\$|US\$|\$|€)\s?\d[\d.,]*"
    r"|\b\d[\d.,]*\s?"
    r"(?:%|k\b|mil\b|mi\b|x\b|h\b|hrs?\b|hours?\b|horas?\b|mins?\b|minutes?\b|minutos?\b"
    r"|seg\b|segundos?\b|days?\b|dias?\b|weeks?\b|semanas?\b|months?\b|meses\b|m[eê]s\b"
    r"|years?\b|anos?\b|reais\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõçà]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
MONEY_RE = re.compile(r"(?:R\$|US\$|\$|€)\s?\d")


def fold(s):
    """minúsculo e sem acento: 'Ninguém' -> 'ninguem'."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip("'’")


def foldset(items):
    return {fold(x) for x in items}


PT_MARK = foldset("que não você voce é de do da um uma pra para com eu meu minha isso "
                  "esse essa mais como mas os as no na seu sua te vc tá ta".split())
EN_MARK = foldset("the and you your is are to of that this it i my with for not don't "
                  "was what how why".split())


def detect_lang(text):
    w = [fold(x) for x in WORD_RE.findall(text)]
    pt = sum(1 for x in w if x in PT_MARK) + 2 * len(re.findall(r"[ãõçáéíóúâêô]", text.lower()))
    en = sum(1 for x in w if x in EN_MARK)
    return "pt" if pt >= en else "en"


LEX = {
    "en": {
        "spoken": foldset("zero two three four five six seven eight nine ten eleven twelve "
                          "fifteen twenty thirty forty fifty sixty seventy eighty ninety hundred "
                          "thousand million billion dozen half twice triple".split()),
        "money": foldset("dollars dollar bucks grand percent cents millionaire billionaire "
                         "revenue profit salary rent".split()),
        "stakes": foldset(
            "stop never wrong mistake mistakes lost lose losing cost costs broke broken failed "
            "failure fail nobody no not don't dont doesn't didn't can't won't quit quitting fired "
            "deleted delete killed kills kill replaced replaces cut beat free paid charged hired "
            "saved first banned illegal worst hate hated wasted waste scam lie lied lying truth "
            "secret hidden stole stolen before until instead but except unless problem risk danger "
            "warning regret wish should shouldn't still already only without versus vs actually".split()),
        "weak": ["so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright", "welcome",
                 "today", "basically", "honestly", "look", "listen", "um", "just", "let", "lets",
                 "let's", "i wanted", "i want", "one of", "have you", "did you", "do you",
                 "are you", "in this", "in today", "the thing", "a lot", "there is", "there are",
                 "this is", "it is", "as a", "when it", "if you've", "you know"],
        "imperatives": foldset("stop steal copy delete try watch read save use build make write "
                               "send take start quit never always don't dont do put run check".split()),
        "you": r"\b(you|your|you're|youre|yourself)\b",
        "me": r"\b(i|my|me|we|our)\b",
        "dealbreakers": [
            (r"(?i)^\s*(?:stop scrolling|don'?t scroll)",
             "Opens with \"stop scrolling\". Asking for attention proves you have not earned it."),
            (r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how)\b",
             "Video preamble. Delete it and open on the payoff."),
            (r"(?i)^\s*(?:hey |hi |what'?s up |welcome )",
             "Greeting. Nobody came to the feed to be greeted."),
        ],
    },
    "pt": {
        "spoken": foldset("zero dois duas três tres quatro cinco seis sete oito nove dez onze doze "
                          "quinze vinte trinta quarenta cinquenta sessenta setenta oitenta noventa "
                          "cem cento duzentos trezentos quinhentos mil milhão milhao milhões milhoes "
                          "bilhão bilhao dúzia metade dobro triplo".split()),
        "money": foldset("reais real conto contos pila grana faturamento faturei faturou lucro "
                         "lucrei salário aluguel porcento milionário bilionário".split()),
        "stakes": foldset(
            "pare nunca jamais errado errada erro erros errei perdi perder perdendo perdeu custou "
            "custa custam quebrei quebrou faliu falhei fracasso fracassei ninguém não nao larguei "
            "demitido demiti apaguei apague apaga matou mata substituiu substitui cortei corta "
            "grátis gratis paguei cobrei contratei economizei primeiro primeira proibido ilegal "
            "pior piores odeio odiei desperdicei desperdício golpe mentira menti mentem verdade "
            "segredo escondido roubei roubado antes até ate mas porém exceto problema risco perigo "
            "cuidado alerta arrependo arrependi deveria ainda já só sem contra versus vs "
            "realmente nenhum nenhuma ninguem".split()),
        "weak": ["oi", "olá", "ola", "e aí", "e ai", "fala galera", "fala pessoal", "fala gente",
                 "galera", "gente", "pessoal", "salve", "bom dia", "boa tarde", "boa noite",
                 "seja bem", "sejam bem", "hoje", "então", "entao", "bom", "tipo", "basicamente",
                 "sinceramente", "olha", "escuta", "é o seguinte", "e o seguinte", "eu queria",
                 "eu quero", "eu vou", "vou te", "um dos", "uma das", "você sabia", "voce sabia",
                 "vocês sabiam", "neste", "nesse", "no vídeo", "isso é", "isso e", "existe",
                 "existem", "tem muita", "quando se", "bem", "enfim", "assim"],
        "imperatives": foldset("pare roube rouba copie copia apague apaga tente tenta teste testa "
                               "assista assiste veja vê leia lê salve salva use usa monte monta "
                               "faça faz escreva escreve mande manda envie pegue pega comece "
                               "começa largue larga nunca sempre não nao coloque coloca rode roda "
                               "confira confere esquece esqueça corta corte".split()),
        "you": r"\b(você|voce|vc|vocês|voces|cê|ce|te|teu|tua|seu|sua|seus|suas|contigo|tu)\b",
        # português esconde o "eu": "Perdi R$ 18 mil" já é primeira pessoa.
        "me": (r"\b(eu|meu|minha|meus|minhas|me|mim|nós|a gente|nosso|nossa|comigo|sou|tô|to|"
               r"estou|tenho|fui|fiz|vou|perdi|aprendi|descobri|vendi|bati|dormi|saí|"
               r"demiti|consegui|\w{2,}ei)\b"),
        "dealbreakers": [
            (r"(?i)^\s*(?:para de rolar|pare de rolar|não pul[ae]|nao pul[ae]|espera,? n[ãa]o)",
             "Abre com \"para de rolar\". Pedir atenção prova que você ainda não ganhou ela."),
            (r"(?i)\b(?:(?:neste|nesse|no) (?:vídeo|video|reels?)(?: de hoje)?|hoje eu vou (?:te )?(?:mostrar|ensinar|falar)|vou te (?:mostrar|ensinar))\b",
             "Preâmbulo de vídeo. Apague e comece pela entrega."),
            (r"(?i)^\s*(?:oi\b|olá|ola\b|e a[ií]\b|fala (?:galera|pessoal|gente)|salve\b|bom dia|boa tarde|boa noite|sejam? bem[- ]vind)",
             "Cumprimento. Ninguém abre o feed pra ser cumprimentado."),
        ],
    },
}

MSG = {
    "pt": {
        "hashtag": "Hashtag no gancho. Hashtag vai no fim da legenda, se for.",
        "emoji": "Emoji no gancho. Texto de gancho na tela tem espaço pra palavras ou pra emoji, não pros dois.",
        "len": "{n} palavras, {c} caracteres, ~{s:.1f}s falado (ideal 5-12 palavras)",
        "conc": "{h} marcador(es) concreto(s)", "conc_none": " - sem número, sem nome, nada checável",
        "stk": "{n} marcador(es) de tensão", "stk_none": " - nada está em jogo nessa frase",
        "price": "um preço", "empty": "vazio",
        "no_payload": "nenhuma palavra forte na frase", "pay1": "palavra forte na posição {i}",
        "pay2": "palavra forte na posição {i}, dava pra trazer pra frente",
        "pay3": "palavra forte na posição {i}, tarde demais", "weak": "; abertura fraca \"{w}\"",
        "you": "fala com quem assiste", "imp": "abre com imperativo (\"{w}\")",
        "me": "primeira pessoa, sem falar com quem assiste", "they": "terceira pessoa, ninguém na sala",
        "title": "NOTA DO GANCHO", "total": "NOTA FINAL","rank": "RANKING DE GANCHOS", "weakest": "mais fraco",
        "deal": "eliminatório", "fix": "Propriedade mais fraca: {w}. Conserte essa e rode de novo.",
        "foot": "Grave o primeiro. Se o primeiro está abaixo de 50, nenhum desses é o gancho ainda.",
        "nothing": "nada pra avaliar",
        "names": {"LENGTH": "TAMANHO", "SPECIFICITY": "CONCRETUDE", "STAKES": "TENSÃO",
                  "FRONTLOAD": "COMEÇO", "ADDRESS": "DESTINO"},
        "verdicts": {"STRONG": "FORTE", "OK": "OK", "WEAK": "FRACO"},
    },
    "en": {
        "hashtag": "Hashtag in the hook. Hashtags belong at the bottom of the caption, if anywhere.",
        "emoji": "Emoji in the hook. On-screen text at hook size has room for words or for an emoji, not both.",
        "len": "{n} words, {c} chars, ~{s:.1f}s spoken (want 5-12 words)",
        "conc": "{h} concrete marker(s)", "conc_none": " - no number, no name, nothing checkable",
        "stk": "{n} tension marker(s)", "stk_none": " - nothing is at stake in this line",
        "price": "a price", "empty": "empty",
        "no_payload": "no payload word anywhere in the line", "pay1": "payload at word {i}",
        "pay2": "payload at word {i}, could move forward", "pay3": "payload at word {i}, too late",
        "weak": "; weak opener \"{w}\"",
        "you": "speaks to the viewer", "imp": "imperative opener (\"{w}\")",
        "me": "first person, no viewer named", "they": "third person, nobody in the room",
        "title": "HOOK SCORE", "total": "HOOK SCORE","rank": "HOOK RANKING", "weakest": "weakest", "deal": "dealbreaker",
        "fix": "Weakest property: {w}. Fix that one and re-run.",
        "foot": "Shoot the top one. If the top one is under 50, none of these are the hook.",
        "nothing": "nothing to score",
        "names": {c: c for c in ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]},
        "verdicts": {"STRONG": "STRONG", "OK": "OK", "WEAK": "WEAK"},
    },
}


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "R$ 18.000" e "$18,000" são uma palavra falada só.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def check_length(text, L, M):
    w = words(text)
    n = len(w)
    secs = n / 2.75
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:
        score -= 12
    return clamp(score), M["len"].format(n=n, c=chars, s=secs)


def check_specificity(text, L, M):
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [fold(w) for w in words(text)]
    spoken = [w for w in low if w in L["spoken"] or w in L["money"]]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, M["conc"].format(h=hits) + (f": {found}" if found else M["conc_none"])


def check_stakes(text, L, M):
    w = [fold(x) for x in words(text)]
    markers = sorted({x for x in w if x in L["stakes"]})
    if MONEY_RE.search(text):
        markers.append(M["price"])
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    return clamp(score), M["stk"].format(n=n) + (f": {', '.join(markers[:4])}" if markers
                                                  else M["stk_none"])


def check_frontload(text, L, M):
    w = words(text)
    if not w:
        return 0.0, M["empty"]
    low = [fold(x) for x in w]
    opener = " ".join(low[:2])
    penalty, hit = 0, None
    for weak in L["weak"]:
        fw = fold(weak)
        if opener == fw or opener.startswith(fw + " ") or low[0] == fw:
            penalty, hit = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in L["stakes"] or token in L["spoken"] or token in L["money"]
                or NUMBER_RE.match(w[i]) and any(ch.isdigit() for ch in w[i])
                or (i and PROPER_RE.match(w[i])) or w[i].startswith(("R$", "$"))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, M["no_payload"]
    elif payload <= 3:
        base, where = 100.0, M["pay1"].format(i=payload + 1)
    elif payload <= 6:
        base, where = 70.0, M["pay2"].format(i=payload + 1)
    else:
        base, where = 40.0, M["pay3"].format(i=payload + 1)
    return clamp(base - penalty), where + (M["weak"].format(w=hit) if hit else "")


def check_address(text, L, M):
    low = text.lower()
    w = [fold(x) for x in words(text)]
    if re.search(L["you"], low):
        return 100.0, M["you"]
    if w and (w[0] in L["imperatives"] or re.match(r"(?i)^\s*para de\b", text)):
        return 90.0, M["imp"].format(w=w[0])
    if re.search(L["me"], low):
        return 70.0, M["me"]
    return 35.0, M["they"]


CHECKS = ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]


def run(text, lang="auto"):
    lang = detect_lang(text) if lang == "auto" else lang
    L, M = LEX[lang], MSG[lang]
    results = {
        "LENGTH": check_length(text, L, M),
        "SPECIFICITY": check_specificity(text, L, M),
        "STAKES": check_stakes(text, L, M),
        "FRONTLOAD": check_frontload(text, L, M),
        "ADDRESS": check_address(text, L, M),
    }
    flags = [msg for rx, msg in L["dealbreakers"] if re.search(rx, text)]
    if HASHTAG_RE.search(text):
        flags.append(M["hashtag"])
    if EMOJI_RE.search(text):
        flags.append(M["emoji"])
    scores = [results[c][0] for c in CHECKS]
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "STRONG" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "WEAK")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, M, out=sys.stdout):
    N, V = M["names"], M["verdicts"]
    print("\n" + M["title"], file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {N[name]:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {M['total']:<13} {bar(overall)} {overall:5.1f}   {V[verdict]}", file=out)
    for f in flags:
        print(f"\n  {M['deal'].upper()}  {f}", file=out)
    if verdict != "STRONG":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print("\n  " + M["fix"].format(w=N[weakest]), file=out)
    print("", file=out)


def render_table(rows, M, out=sys.stdout):
    N, V = M["names"], M["verdicts"]
    print("\n" + M["rank"] + "\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {V[r['verdict']]:<7} {hook}", file=out)
        print(f"        {M['weakest']}: {N[r['weakest']]} "
              f"({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        {M['deal']}: {f}", file=out)
    print("\n" + M["foot"] + "\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota para ganchos de Reel em cinco propriedades.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo com um gancho por linha, ou -")
    ap.add_argument("--hook", help="avaliar um gancho só, direto na linha de comando")
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    lang = args.lang if args.lang != "auto" else detect_lang("\n".join(lines))
    M = MSG[lang]
    if not lines:
        print(M["nothing"], file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, lang)
        payload.append({
            "hook": line,
            "lang": lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], lang)
        render_one(lines[0], results, overall, verdict, flags, M)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]), M)

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
