#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JOA00FC - coleta SOMENTE tres FastFiles do MW2 PC (IW4) para adaptar PT-BR.

NAO modifica o jogo, nao faz upload automatico, nao coleta saves.
Os arquivos FF contem dados proprietarios: envie o ZIP apenas em canal privado
para diagnostico, NAO publique o ZIP no GitHub ou em servidores publicos.
"""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import os
import struct
import sys
import zipfile

FILES = ("common.ff", "code_post_gfx.ff", "patch.ff")
GAME = "/storage/emulated/0/X360/Call of Duty - Modern Warfare 2"
OUTPUT = "/storage/emulated/0/Download/MW2_BASE_LIMPA_PARA_ADAPTAR_PTBR.zip"
EXPECTED = {
    "common.ff": "f109313cc652fa1890223966bdb52157dd620f18183ccf4c4350cf61ed0c5e35",
    "code_post_gfx.ff": "1802c26386e08cb17660f19d3f511b89e081dfbbed8ad04b360f62fd5c6ae047",
    "patch.ff": "11be5452fa0f40aa7169c7a04810f9a5df8c0c782d0e9e403159159a322735c1"
}

def hash_file(path):
    h=hashlib.sha256()
    with path.open("rb") as file:
        for b in iter(lambda:file.read(4*1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pasta",default=GAME)
    p.add_argument("--saida",default=OUTPUT)
    args=p.parse_args()
    source=Path(args.pasta).expanduser().resolve()/"zone"/"english"
    out=Path(args.saida).expanduser()
    if not source.is_dir():
        raise SystemExit("Nao foi encontrada a pasta zone/english no caminho informado.")
    if out.exists():
        raise SystemExit("O ZIP de saida ja existe. Renomeie-o ou mova-o para preservar a copia anterior: "+str(out))
    rows=[]
    paths=[]
    for name in FILES:
        path=source/name
        if not path.is_file() or path.is_symlink():
            raise SystemExit("Arquivo ausente ou invalido: "+str(path))
        with path.open("rb") as f:
            header=f.read(12)
        if len(header)<12 or header[:8]!=b"IWffu100" or struct.unpack_from("<I",header,8)[0]!=276:
            raise SystemExit("O arquivo nao e um FastFile IW4 conhecido: "+name)
        size=path.stat().st_size
        if size>300_000_000 or size<100:
            raise SystemExit("Tamanho inesperado para "+name)
        digest=hash_file(path)
        if digest != EXPECTED[name]:
            raise SystemExit("A base nao confere com o relatorio da instalacao limpa em: "+name
                             +"\nEsperado: "+EXPECTED[name]+"\nEncontrado: "+digest
                             +"\nNao tente usar a traducao de outra versao.")
        rows.append({"file":name,"size_bytes":size,"sha256":digest})
        paths.append(path)
        print("Conferido:",name, f"{size/1_000_000:.1f} MB", digest[:16])
    out.parent.mkdir(parents=True,exist_ok=True)
    temp=out.with_name(out.name+".tmp")
    if temp.exists():
        raise SystemExit("Ja existe um ZIP temporario. Remova-o manualmente se foi deixado por uma execucao anterior: "+str(temp))
    report={
        "project":"JOA00FC MW2 2009 PC IW4 - base limpa para adaptar traducao",
        "date":datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_folder":str(source),
        "items":rows,
        "changed_game_files":False,
        "contains_proprietary_game_data":True,
        "warning":"NAO publique este ZIP no GitHub ou em rede publica. Compartilhe apenas em privado com quem adaptara a traducao."
    }
    try:
        with zipfile.ZipFile(temp,"w",compression=zipfile.ZIP_STORED,allowZip64=True) as z:
            for name,path in zip(FILES,paths):
                z.write(path,arcname="base/"+name)
            z.writestr("RELATORIO_BASE_LIMPA.json",json.dumps(report,indent=2,ensure_ascii=False)+"\n")
            z.writestr("LEIA_PRIMEIRO.txt","ZIP para diagnostico privado. Contem arquivos proprietarios do jogo. NAO publique. Nenhum arquivo do jogo foi modificado.\n")
        os.replace(temp,out)
    except Exception:
        if temp.exists():temp.unlink()
        raise
    print("\nCRIADO:",out)
    print("Arquivos do jogo preservados. Envie este ZIP no chat para adaptacao PT-BR.")
    print("Nao publique o ZIP em repositorios publicos.")

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:sys.exit("Operacao cancelada; jogo nao alterado.")
