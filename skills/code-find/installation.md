# Installing and Configuring cfind

Read this file only when `cfind` is unavailable or `CFIND_ROOT` is missing or invalid.

## Install the CLI

If `cfind` is already available, skip to configuration.

1. Check that Git and a compatible Rust toolchain are available. `git --version`, `cargo --version`, and `rustc --version` must succeed. Current cfind source requires Rust 1.88 or newer.
2. If Git or Rust is unavailable or too old, report the prerequisite and ask before installing or updating it. If approved, use its official platform installation method, then continue; otherwise stop.
3. Clone `https://github.com/vincepr/cfind.git` into a writable build directory. Do not overwrite an existing checkout or modify a dirty one.
4. In the clone, run `cargo build --release`.
5. Run `cargo install --path .`.
6. Verify `cfind --version`. If the command is still unavailable, add Cargo's binary directory to the user's persistent `PATH` and retry in a fresh shell.

## Configure the Search Root

`CFIND_ROOT` is required and should point to the directory containing the repositories the user wants searched.

1. Ask the user which folder contains their owned, team, or company repositories.
2. Confirm that the selected path exists and is a directory.
3. Set `CFIND_ROOT` for the current setup commands.
4. Persist `CFIND_ROOT` in the user's environment using the platform's standard user-level mechanism.

On POSIX shells, update the active shell's startup file with an exported `CFIND_ROOT`, replacing an existing assignment instead of adding duplicates. On Windows PowerShell, set both the current process value and the user environment value. Preserve unrelated environment and profile content.

The current agent process may not observe a newly persisted parent-shell environment. Tell the user to restart their shell or agent after setup.

## Initialize and Verify

With `CFIND_ROOT` set for the command:

1. Run `cfind --index`.
2. Run `cfind --type` and confirm symbol kinds are present when supported repositories exist under the configured root.

Do not configure optional language, index-path, or freshness variables unless the user requests different defaults.

## Optional Session Finder

After cfind is working, ask whether the user also wants to install [sfind](https://github.com/vincepr/sfind), a local finder for Codex, OpenCode, and Claude Code sessions.

If accepted and `sfind` is not already available:

1. Clone `https://github.com/vincepr/sfind.git` into a writable build directory without overwriting an existing or dirty checkout.
2. Run `cargo build --release` in the clone.
3. Run `cargo install --path .`.
4. Verify `sfind --version`.

sfind needs no additional setup; it discovers the providers' standard session locations automatically.
