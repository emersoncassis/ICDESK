#!/usr/bin/env python3
"""Troca o nome visível do app (ICDESK) e o da empresa (IC TEAM) pelos da sua marca.

Uso (na raiz do repositório):
    python3 .agents/skills/acesso-remoto-1-marca/scripts/renomear_marca.py "MeuDesk" "Minha Empresa"
        -> só mostra o que mudaria (simulação)
    python3 .../renomear_marca.py "MeuDesk" "Minha Empresa" --aplicar
        -> grava as mudanças

Não toca em nomes internos: ICDESK_SERVER, ICDESK_KEY, src/icdesk.rs, pacote Android,
nem nas pastas de skills, site, docs e no gerador de marca.
"""
import re
import subprocess
import sys

IGNORAR = (".agents/", ".claude/", "site/", "docs/", "res/icdesk-brand/", "deploy/", ".github/")
NOME = re.compile(r"(?<![A-Za-z0-9_])ICDESK(?!_)")
EMPRESA = re.compile(r"\bIC TEAM\b")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    nome, empresa = args
    aplicar = "--aplicar" in sys.argv
    arquivos = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
    total = 0
    for f in arquivos:
        if not f or f.startswith(IGNORAR) or f == "src/icdesk.rs":
            continue
        try:
            txt = open(f, encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        novo = EMPRESA.sub(empresa, NOME.sub(nome, txt))
        if novo != txt:
            n = len(NOME.findall(txt)) + len(EMPRESA.findall(txt))
            total += n
            print(f"{n:5}  {f}")
            if aplicar:
                open(f, "w", encoding="utf-8").write(novo)
    print(f"\n{total} trocas" + ("" if aplicar else " (simulação; rode de novo com --aplicar)"))


if __name__ == "__main__":
    main()
