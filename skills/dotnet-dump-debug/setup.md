# dotnet-dump Setup

Read this file only when `dotnet-dump` or the optional `dbg` shim is unavailable.

## Install

The bundled installer installs Microsoft's `dotnet-dump` global tool and creates an optional `dbg` shim in `~/.local/bin`:

```bash
bash <skill-directory>/scripts/install.sh
```

Ask before installing tools or writing the shim. No administrator privileges are required.

Alternatively, install only the .NET tool:

```bash
dotnet tool install --global dotnet-dump
```

## Verify

```bash
dotnet-dump --version
python3 <skill-directory>/scripts/dbg.py --help
```

If the `dbg` shim is not found, invoke `scripts/dbg.py` directly or add `~/.local/bin` to `PATH`.

## Uninstall

Stop any active session first, then remove only the installed components:

```bash
dbg stop
dotnet tool uninstall --global dotnet-dump
rm ~/.local/bin/dbg
```

Session logs and retained dumps remain under `${XDG_CACHE_HOME:-~/.cache}/dotnet-debug` until explicitly removed.
