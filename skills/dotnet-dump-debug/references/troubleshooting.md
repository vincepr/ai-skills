# dotnet-dump Troubleshooting

## Logs

Each session stores these files under `${XDG_CACHE_HOME:-~/.cache}/dotnet-debug/sessions/<repository-hash>/`:

- `collect.log` — `dotnet-dump collect` output.
- `daemon.log` — helper daemon output and Python tracebacks.
- `target.json` — process ID, label, and dump options.
- `snapshot.dmp` — the dump, deleted by `stop` unless retained.

## Collection Fails

- Confirm the PID belongs to a supported .NET process.
- Run the helper as the same user as the target process.
- Check available disk space; full dumps can be several gigabytes.
- Read `collect.log` for the exact diagnostic error.

## Analysis Is Slow

The first command loads SOS and the DAC. Later commands reuse the same analyzer. Heap enumeration can still be slow; start with `heap --stat` or filter by type.

## Stacks Lack Source Locations

Build with portable PDBs and keep the `.pdb` files beside the assemblies. Methods remain visible without PDBs, but file and line information does not.

## No Active Snapshot

Sessions are keyed by repository root. Run all commands from the same working directory and create a new snapshot if the previous session was stopped.

## Stale Session

Try `dbg stop` first. If the daemon is no longer reachable, inspect `daemon.pid` and `daemon.log` in the session directory before removing only that stale session directory.

## Breakpoints and Stepping

This helper intentionally uses offline snapshots. It does not provide breakpoints or stepping. Use a supported IDE debugger when interactive debugging is required.

Snapshot analysis is particularly useful where attaching a live CLI debugger is unsupported or unreliable. Avoid presenting platform-specific debugger limitations as universal; tool and runtime support changes over time.
