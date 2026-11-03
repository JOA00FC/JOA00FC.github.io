#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JOA00FC | MW2 (2009) PC IW4 | Verificacao nao destrutiva da instalacao.
Nao edita, renomeia, restaura nem substitui arquivos. Gera um relatorio ZIP.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import os
import struct
import sys
import zipfile
from datetime import datetime

GAME_DEFAULT = "/storage/emulated/0/X360/Call of Duty - Modern Warfare 2"
OUTPUT_DEFAULT = "/storage/emulated/0/Download/MW2_BASE_NOVA_RELATORIO.zip"
FILES = ("common.ff", "code_post_gfx.ff", "patch.ff", "trainer.ff", "roadkill.ff")
KNOWN = {
    "common.ff": {
        "f715f4ca5f2449217979d11d91b163762f7addf00229c43e31ba1c83a10da73f": "base anterior enviada para diagnostico",
        "5bd2404dd54bc462d56b9ce429f40452dd3be081182c5e87f0a53528c7e13899": "traducao V5",
        "059733fde8bbb793e2e4e33253360d0b0f55d491e2790690474360eb64cf1f7f": "traducao cutscenes V6"
    },
    "code_post_gfx.ff": {
        "6f189e840147fe03cec10e3d08c77b7cfbf6cb715c2415f433fd6769b49c1a78": "base anterior enviada para diagnostico",
        "2c3b5fc5fd87eaaa2f7d53099b6b78e5da91dcb1cf3d9127f9a52857cb8e350e": "traducao V5"
    },
    "patch.ff": {
        "11be5452fa0f40aa7169c7a04810f9a5df8c0c782d0e9e403159159a322735c1": "base antiga de patch.ff (nao necessariamente original do jogo)",
        "4739cfba80fa08443bddd4d39898c4ba5a31c8676e50b7675acc4beb633f67d1": "base GameHub enviada anteriormente",
        "7f12b70e87d3b6710d5031d8030bd4a0b2f59ebe8ed9a99835c44e5d76629765": "traducao V4",
        "c012b00499fa7f1295736fba7930ad9c4c845b6b1c556783991ab47210d6abbc": "traducao V5/V6"
    },
    "trainer.ff": {
        "ea39af07c68258e7e129b48ffb2c0494b2f30fa7f902532c30a7002e3513be54": "mesmo arquivo de S.S.D.D. da instalacao anterior"
    },
    "roadkill.ff": {
        "122c1d9db5c016aacf65ddb1846f090e9328a7164d586d34660dd4d3e3b1056f": "mesmo arquivo de Team Player da instalacao anterior (nao significa erro)"
    }
}

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def inspect(path, name):
    data = {"file": name, "present": path.is_file() and not path.is_symlink()}
    if not data["present"]:
        data["error"] = "ausente ou link simbolico"
        return data
    try:
        st = path.stat()
        with path.open("rb") as f:
            head = f.read(23)
        data["size_bytes"] = st.st_size
        data["signature"] = head[:8].decode("ascii", errors="replace")
        data["version"] = struct.unpack_from("<I", head, 8)[0] if len(head) >= 12 else None
        data["zlib_prefix"] = head[21:23].hex() if len(head) >= 23 else None
        data["header_iw4"] = data["signature"] == "IWffu100" and data["version"] == 276
        data["sha256"] = digest(path)
        data["reference_match"] = KNOWN.get(name, {}).get(data["sha256"], "nao listado no historico")
        data["note"] = "cabecalho e SHA-256 nao comprovam compatibilidade ou recursos internos"
    except (OSError, ValueError, struct.error) as exc:
        data["error"] = type(exc).__name__ + ": " + str(exc)
    return data

def main():
    parser = argparse.ArgumentParser(description="MW2 PC 2009 / GameHub - verifica instalacao sem modificar o jogo")
    parser.add_argument("--pasta", default=GAME_DEFAULT, help="pasta do jogo")
    parser.add_argument("--saida", default=OUTPUT_DEFAULT, help="destino do relatorio ZIP")
    args = parser.parse_args()
    game = Path(args.pasta).expanduser()
    english = game / "zone" / "english"
    print("\nJOA00FC - DIAGNOSTICO LIMPO DO MW2 2009 PC")
    print("Pasta:", game)
    if not english.is_dir():
        raise SystemExit("ERRO: nao encontrei zone/english; confira a pasta, sem alterar nada.")
    rows = []
    for filename in FILES:
        print("Conferindo", filename, "...", flush=True)
        rows.append(inspect(english / filename, filename))
        label = rows[-1].get("reference_match", rows[-1].get("error", ""))
        print(" ->", label)
    iwd = sorted((game / "main").glob("*.iwd")) if (game / "main").is_dir() else []
    summary = {
        "project": "MW2 PT-BR JOA00FC - verificacao previa (somente leitura)",
        "generated_at_local": datetime.now().astimezone().isoformat(timespec="seconds"),
        "game_folder": str(game),
        "gamehub_note": "Teste Team Player na instalacao limpa ANTES de aplicar a traducao",
        "zone_english_ff_count": len(list(english.glob("*.ff"))),
        "main_iwd_count": len(iwd),
        "main_iwd_names": [f.name for f in iwd],
        "files": rows,
        "translation_applied_by_this_tool": False,
        "limitations": [
            "Nenhum arquivo foi modificado.",
            "SHA-256 e cabeçalho nao garantem funcionamento das missoes.",
            "Arquivos nao listados no historico nao sao necessariamente incorretos."
        ]
    }
    out = Path(args.saida).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    temp = out.with_name(out.name + ".tmp")
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("MW2_BASE_NOVA_RELATORIO.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
            z.writestr("LEIA_PRIMEIRO.txt",
                       "Este ZIP so contem hashes e inventario (sem dados do jogo). "
                       "Envie ao ChatGPT antes de instalar traducao.\n")
        os.replace(temp, out)
    finally:
        if temp.exists():
            temp.unlink()
    print("\nRELATORIO CRIADO:", out)
    print("Nenhum arquivo do jogo foi alterado.")
    print("TESTE: abra Team Player na instalacao nova antes de aplicar a traducao.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrompido. Nenhum arquivo do jogo foi alterado.")
