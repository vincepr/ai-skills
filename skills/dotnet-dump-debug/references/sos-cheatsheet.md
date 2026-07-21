# SOS and dotnet-dump analyze Cheatsheet

`dbg` commands run SOS commands inside a persistent `dotnet-dump analyze <dump>` session. Run other SOS commands with `dbg sos "<raw-command>"`.

## Command Mapping

| `dbg` command | SOS command |
|---|---|
| `stack` / `stack --all` / `stack --args` | `clrstack` / `clrstack -all` / `clrstack -a` |
| `pstacks` | `pstacks` |
| `threads` | `clrthreads` |
| `heap --stat` / `heap --type T` | `dumpheap -stat` / `dumpheap -type T` |
| `obj <address>` | `dumpobj <address>` |
| `dso` | `dso` |
| `sos "<raw-command>"` | `<raw-command>` |

## Useful SOS Commands

| Command | Use |
|---|---|
| `dumparray <address>` | Display managed array elements |
| `gcroot <address>` | Find why an object remains reachable |
| `dumpheap -type <T> -stat` | Count and size instances of a type |
| `dumpheap -mt <MT> -min 1000` | Find larger instances of a method table |
| `dumpasync` | Inspect async state machines |
| `dumpmd <address>` / `dumpmt <address>` | Inspect a MethodDesc or MethodTable |
| `dumpdomain` | List assemblies and AppDomains |
| `eeheap -gc` | Summarize GC heap segments and sizes |
| `syncblk` | Inspect monitor locks and synchronization blocks |
| `setthread <id>` then `clrstack` | Switch the current thread and inspect its stack |
| `printexception` / `pe <address>` | Inspect a managed exception |
| `name2ee <module> <type>` | Resolve a type or method |

## Notes

- `setthread <osid>` changes the current thread for `clrstack` and `dso`; `stack --all` inspects every thread without switching.
- Source locations require portable PDBs beside the analyzed assemblies.
- `clrstack -a` exposes argument and local addresses and values, but local names may be unavailable.
- Run `dbg sos "soshelp <command>"` for command-specific help.
- A session analyzes a fixed snapshot. Use `dbg resnapshot` to inspect a later moment.
