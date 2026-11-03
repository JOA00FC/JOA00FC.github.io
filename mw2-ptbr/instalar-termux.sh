#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
BASE='https://joa00fc.github.io/mw2-ptbr'
PACKAGE='MW2_PTBR_FONTES_V1.zip'
GAME='/sdcard/X360/Call of Duty - Modern Warfare 2'
WORK="$HOME/mw2-ptbr-builder"
if [ ! -f "$GAME/zone/english/common.ff" ]; then
 echo 'MW2 nao encontrado em /sdcard/X360. Ajuste GAME para sua pasta.' >&2; exit 1
fi
pkg install -y python curl unzip proot-distro qemu-user-i386
mkdir -p "$WORK/fonte"
curl -fL --retry 3 "$BASE/download/$PACKAGE" -o "$WORK/$PACKAGE"
unzip -oq "$WORK/$PACKAGE" -d "$WORK/fonte"
python "$WORK/fonte/REBUILD.py" --pasta "$GAME" --verificar
case "${1:---verificar}" in
 --verificar) echo 'Verificacao concluida. Nenhum arquivo foi alterado.' ;;
 --restaurar) python "$WORK/fonte/REBUILD.py" --pasta "$GAME" --restaurar ;;
 *) echo 'Instalacao automatica ARM64/i386 ainda nao homologada. Nao foram substituidos arquivos FF.'; exit 2 ;;
esac
