---
name: dotnet-dump-debug
description: Inspect a running .NET process with dotnet-dump snapshots. Use for managed hangs, leaks, high CPU or memory, stacks, heap objects, and runtime state.
disable-model-invocation: true
---

# Debug .NET Processes with dotnet-dump

Inspect managed call stacks, threads, the GC heap, and object fields from a process snapshot. The bundled helper keeps a `dotnet-dump analyze` session alive across commands and returns JSON.

This is snapshot inspection, not live breakpoint debugging. Capture a fresh snapshot with `resnapshot` to inspect a later moment.

## Prerequisites

Check for `dotnet-dump` before the first snapshot. If it is missing, read [setup.md](setup.md) and complete the setup with the user's approval.

Resolve `scripts/dbg.py` relative to this skill directory. The examples below use `dbg` for either that Python script or the optional installed shim. Run commands for one session from the same working directory because sessions are keyed by repository root.

## Capture a Snapshot

One active session is allowed per repository:

```bash
dbg snapshot <pid>
dbg snapshot --name "<process-name-substring>"
dbg snapshot --launch <project-or-dll> [--delay <seconds>] [-- <arguments>]
```

Use `--full` only when native state is required; full dumps can be large. Use `--keep-dump` only when the dump must survive `stop`.

Choose the capture point deliberately:

- Snapshot a process as-is when it is hung, leaking, or consuming excessive resources.
- For transient state, use `resnapshot` or arrange an intentional pause in development code.
- For tests, pause at the relevant point and snapshot the matching test process.

## Inspect Managed State

```bash
dbg stack [--all] [--args]
dbg pstacks
dbg threads
dbg heap --stat [--type <TypeName>]
dbg dso
dbg obj <address>
dbg sos "<raw-sos-command>"
```

Stacks include source locations when portable PDBs are available beside the assemblies.

To inspect a value, start with `stack`, locate candidate objects with `dso` or `heap --type`, then inspect an address with `obj`. Use `dbg sos "dumparray <address>"` for arrays. Read [references/sos-cheatsheet.md](references/sos-cheatsheet.md) for more commands.

## Refresh and Clean Up

```bash
dbg resnapshot
dbg status
dbg stop
```

Always run `stop` when finished or after a failure. It ends the analyzer and deletes the dump unless `--keep-dump` was selected.

Report conclusions in plain language rather than returning an unexplained SOS dump.

## Guardrails

- Confirm the target before snapshotting; do not inspect an unrelated process.
- Mention that dump collection may briefly pause the target and that dumps can contain sensitive application data.
- Do not retain or share a dump unless the user explicitly asks.
- Offer an IDE debugger when the task requires breakpoints or stepping.
- Read [references/troubleshooting.md](references/troubleshooting.md) when collection or analysis fails.

Session logs are stored under `${XDG_CACHE_HOME:-~/.cache}/dotnet-debug/sessions/<repository-hash>/`.
