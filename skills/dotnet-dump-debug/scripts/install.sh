#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { printf '[dotnet-dump setup] %s\n' "$*"; }
fail() { printf '[dotnet-dump setup] ERROR: %s\n' "$*" >&2; exit 1; }

command -v dotnet >/dev/null 2>&1 || fail "dotnet SDK not found on PATH"

if dotnet tool list --global 2>/dev/null | grep -qi '^dotnet-dump'; then
  log "dotnet-dump is already installed"
else
  log "installing dotnet-dump"
  dotnet tool install --global dotnet-dump
fi

DOTNET_DUMP="$HOME/.dotnet/tools/dotnet-dump"
if [ ! -x "$DOTNET_DUMP" ]; then
  DOTNET_DUMP="$(command -v dotnet-dump || true)"
fi
[ -n "$DOTNET_DUMP" ] || fail "dotnet-dump not found after installation"
"$DOTNET_DUMP" --version >/dev/null

SHIM_DIR="$HOME/.local/bin"
mkdir -p "$SHIM_DIR"
{
  printf '#!/usr/bin/env bash\n'
  printf 'exec python3 %q "$@"\n' "$SCRIPT_DIR/dbg.py"
} > "$SHIM_DIR/dbg"
chmod +x "$SHIM_DIR/dbg"

log "installed dbg shim at $SHIM_DIR/dbg"
log "ensure $SHIM_DIR is on PATH, or invoke $SCRIPT_DIR/dbg.py directly"
