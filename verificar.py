#!/usr/bin/env python3
"""
verificar.py - confere se o pacote está funcionando na sua máquina.

Roda as cinco ferramentas nos arquivos de exemplo e diz OK ou FALHOU pra cada
uma. Não precisa instalar nada, não usa internet.

    python verificar.py          (Windows)
    python3 verificar.py         (Mac / Linux)

Pode rodar de dentro da pasta do repositório ou da pasta onde as skills foram
instaladas (ex.: ~/.claude/skills): ele procura as skills nos dois lugares.
"""

import json
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [os.path.join(HERE, "skills"), HERE,
              os.path.join(os.path.expanduser("~"), ".claude", "skills")]
SKILLS = next((c for c in CANDIDATES if os.path.isdir(os.path.join(c, "ig-reel"))), None)
EX = os.path.join(HERE, "exemplos")

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"  {'OK     ' if ok else 'FALHOU '} {name}" + (f"  ({detail})" if detail else ""))


def run(script, *args, stdin=None):
    p = subprocess.run([sys.executable, os.path.join(SKILLS, script), *args],
                       input=stdin, capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def main():
    print("\nVERIFICAÇÃO DO PACOTE INSTAGRAM (PT-BR)\n" + "=" * 44)
    check("Python 3.8 ou mais novo", sys.version_info >= (3, 8), sys.version.split()[0])
    if not SKILLS:
        check("pasta das skills encontrada", False,
              "rode este arquivo de dentro da pasta do repositório")
        return finish()
    check("pasta das skills encontrada", True, SKILLS)

    names = ["ig-audit", "ig-caption", "ig-carousel", "ig-comment", "ig-dm", "ig-human",
             "ig-plan", "ig-profile", "ig-reel", "ig-reply", "ig-repurpose", "ig-story",
             "ig-viral", "ig-voz"]
    missing = [n for n in names if not os.path.isfile(os.path.join(SKILLS, n, "SKILL.md"))]
    check(f"{len(names)} skills com SKILL.md", not missing, ", ".join(missing) or "todas presentes")

    hooks = [
        "Ninguém te conta que seus primeiros 30 reels vão flopar",
        "Oi gente, hoje eu quero falar sobre estratégia de conteúdo",
    ]
    code, out, err = run("ig-reel/hookscore.py", "--json", "-", stdin="\n".join(hooks))
    try:
        data = json.loads(out)
        ok = data[0]["score"] > 70 and data[1]["score"] < 30
        check("hookscore.py (nota de gancho em português)", ok,
              f"{data[0]['score']} vs {data[1]['score']}")
    except Exception:
        check("hookscore.py", False, (err or out)[-200:])

    if os.path.isdir(EX):
        code, out, err = run("ig-reel/beats.py", os.path.join(EX, "roteiro.txt"), "--json")
        try:
            data = json.loads(out)
            check("beats.py (tempos do roteiro)", data["total_seconds"] > 10,
                  f"{data['total_seconds']}s")
        except Exception:
            check("beats.py", False, (err or out)[-200:])

        code, out, err = run("ig-caption/caption.py", os.path.join(EX, "legenda-humana.txt"), "--json")
        try:
            data = json.loads(out)
            check("caption.py (revisão de legenda)", data["truncated"] and len(data["hashtags"]) == 3)
        except Exception:
            check("caption.py", False, (err or out)[-200:])

        code, out, err = run("ig-human/humanize.py", os.path.join(EX, "legenda-ia.txt"), "--json")
        try:
            data = json.loads(out)
            ok = data["report"]["lang"] == "pt" and "alavancar" not in data["text"].lower()
            check("humanize.py (tira cara de IA)", ok,
                  f"{len(data['report']['lexical'])} termos trocados")
        except Exception:
            check("humanize.py", False, (err or out)[-200:])

        code, out, err = run("ig-human/detect.py", os.path.join(EX, "legenda-ia.txt"),
                             os.path.join(EX, "legenda-humana.txt"), "--json")
        try:
            a, b = json.loads(out)
            check("detect.py (painel de detecção)", a["human_score"] < 50 < b["human_score"],
                  f"IA {a['human_score']} vs humana {b['human_score']}")
        except Exception:
            check("detect.py", False, (err or out)[-200:])

        code, out, err = run("ig-viral/swipe.py", os.path.join(EX, "coletados.tsv"), "--json")
        try:
            data = json.loads(out)
            check("swipe.py (ranking de virais)", data["reels"][0]["formula_id"] == 9,
                  f"{data['n']} reels")
        except Exception:
            check("swipe.py", False, (err or out)[-200:])
    else:
        print("  (pasta exemplos/ não encontrada, testes de arquivo pulados)")

    return finish()


def finish():
    print("-" * 44)
    if all(results):
        print("  TUDO CERTO. Abra o Claude Code e digite /ig-voz pra começar.\n")
        return 0
    print("  Algo falhou. Copie esta tela e mande pra quem te passou o pacote.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
