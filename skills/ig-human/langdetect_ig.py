"""Detecção de idioma mínima (pt / en), compartilhada por humanize.py e detect.py.

Sem dependências. Conta palavras-marcadoras e acentos. É só pra decidir qual
bloco do slop.json aplicar, não precisa ser perfeito.
"""

import re
import sys
import unicodedata


def utf8_console():
    """Windows: o console padrão (cp1252) quebra com emoji e acentos."""
    for s in (sys.stdin, sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


_W = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")
_PT = {fold(x) for x in "que não você é de do da um uma pra para com eu meu minha isso esse essa "
                        "mais como mas os as no na seu sua te vc tá né a gente".split()}
_EN = set("the and you your is are to of that this it i my with for not don't was what how why".split())


def detect_lang(text):
    w = [fold(x) for x in _W.findall(text)]
    pt = sum(1 for x in w if x in _PT) + 2 * len(re.findall(r"[ãõçáéíóúâêô]", text.lower()))
    en = sum(1 for x in w if x in _EN)
    return "pt" if pt >= en else "en"


def entries_for(lex, key, lang):
    return [e for e in lex[key] if e.get("lang", "en") in (lang, "any")]
