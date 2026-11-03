#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
BASE='https://joa00fc.github.io/mw2-ptbr'
GAME="${MW2_GAME_DIR:-/sdcard/X360/Call of Duty - Modern Warfare 2}"
MODE="${1:---verificar}"
case "$MODE" in
  --verificar)
    if ! command -v python >/dev/null 2>&1; then echo "Instale Python: pkg install python" >&2; exit 1; fi
    curl -fL --retry 3 "$BASE/verificar-gamehub.py" -o "$HOME/mw2-verificar.py"
    python "$HOME/mw2-verificar.py" --pasta "$GAME"
    ;;
  --instalar)
    echo "Instalacao automatica no Termux ainda nao homologada. Nenhum FF foi alterado." >&2
    exit 2
    ;;
  --restaurar)
    echo "Use o instalador que criou o backup. Este script apenas verifica." >&2
    exit 2
    ;;
  *) echo "Uso: bash instalar-termux.sh --verificar" >&2; exit 2 ;;
esac
