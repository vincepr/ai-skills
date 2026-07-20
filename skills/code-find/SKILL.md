---
name: code-find
description: Use the cfind CLI to find local and GitHub/GitLab source locations for classes, functions, namespaces, and reusable code across user or company repositories.
---

# code-find

Use `cfind` to search a local index of symbols across owned repositories before reimplementing code or adding another dependency.

The index covers Git-tracked files in cfind's enabled supported languages. Disabled, unsupported, or untracked source is not searched.

## Before Searching

Check that `cfind` is available and `CFIND_ROOT` names an existing directory. If either is missing or invalid, read [installation.md](installation.md) and complete only the missing setup. Otherwise, do not load the installation reference.

Use `cfind --help` for the current CLI and `cfind --type` to list symbol kinds in the active index.

## Search

- Search by symbol name with `cfind NAME`. Matching is fuzzy and exact names rank first.
- Restrict a symbol kind with `cfind NAME --type KIND`.
- Search a namespace declaration with `cfind NAMESPACE --type namespace`.
- To search for a class, record, function, method, interface, or another declaration, choose its current kind from `cfind --type`. Do not assume callable kinds are identical across languages.
- Add `--verbose` when containing namespaces help distinguish similarly named C# symbols. Namespace is displayed metadata, not a namespace filter for other symbol kinds.
- Narrow by repository-relative path with `--filter REGEX`.
- Use `--from DIRECTORY` to prefer nearby repositories and paths when name ranking is otherwise comparable; proximity is especially important for exact-name matches.
- Use `--limit`, `--quiet`, or `--commit-url` when the task needs different output volume or links.

Results contain the symbol kind, name, local file and line, and usually a repository URL. Open the local result to inspect the implementation before deciding to reuse it.

## Index

`cfind` creates or refreshes its index automatically when required. Use `cfind --status` to inspect it and `cfind --index` after branch or commit changes when results or links must be current immediately.
