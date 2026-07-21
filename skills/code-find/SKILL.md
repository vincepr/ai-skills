---
name: code-find
description: Use the cfind CLI to find local and GitHub/GitLab source locations for classes, functions, namespaces, and reusable code across user or company repositories.
---

# code-find

Use `cfind` to search a local index of symbols across owned repositories before reimplementing code or adding another dependency.

The index covers Git-tracked files in cfind's enabled supported languages. Disabled, unsupported, or untracked source is not searched.

## Before Searching

Check that `cfind` is available and `CFIND_ROOT` names an existing directory. If either is missing or invalid, read [setup.md](setup.md) and complete only the missing setup. Otherwise, do not load the setup reference.

Use `cfind --help` for the current CLI.

## Search

- Start with `cfind NAME` and no filters. It searches all symbol kinds and ranks exact short names strongest.
- Use `cfind NAME --rough` to find relevant repositories and code areas. Within each repository, it collapses a matched namespace and its members, or matches sharing a full enclosing type, before `--limit`.
- Add context with terms (`cfind Acme Tools PaymentProcessor`) or a qualified name (`cfind Acme.Tools.PaymentProcessor`). Terms match short and qualified names; complete coverage ranks above partial matches.
- Use `--type KIND` only when results contain the wrong declaration kind and that distinction matters. If needed, `cfind --type` lists the kinds available in the current index.
- Distinct qualified names appear by default for all supported languages; use them to distinguish similar short names. Identical names appear once.
- Compose terms with `--filter REGEX` for repository-relative paths, `--from PATH` for proximity among comparable results (default: current directory), `--limit` for count, `--quiet` for no URLs, or `--commit-url` to prefer commit-pinned links. Options may appear around terms.

Results give kind, short name, any distinct qualified name, local file and one-based line, match score/state metadata, and usually a repository URL. Open the local result before reuse.

A valid no-match search exits `1`, leaves stdout empty, and explains the miss on stderr; do not treat it as a CLI or index failure.

## Index

`cfind` manages index freshness automatically and warns when an index is stale. Use `cfind --index` only when an immediate refresh is needed.
