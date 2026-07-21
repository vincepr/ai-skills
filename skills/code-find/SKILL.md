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

- Start with `cfind NAME`. It searches all symbol kinds, uses fuzzy matching, ranks exact names first, and labels each result with its kind.
- Keep searches unfiltered by default, including searches for namespaces, classes, records, interfaces, methods, and functions.
- Use `--type KIND` only when results contain the wrong declaration kind and that distinction matters. If needed, `cfind --type` lists the kinds available in the current index.
- C# records and interfaces appear as distinct `record` and `interface` results without requiring a type filter.
- Add `--verbose` when containing namespaces help distinguish similarly named C# symbols. Namespace is displayed metadata, not a namespace filter for other symbol kinds.
- Narrow by repository-relative path with `--filter REGEX`.
- Use `--limit` or `--quiet` when the task needs different output volume.
- Use `--commit-url` when sharing or citing an exact source location from a pushed commit or feature branch.

Results contain the symbol kind, name, local file and line, and usually a repository URL. Open the local result to inspect the implementation before deciding to reuse it.

## Index

`cfind` manages index freshness automatically and warns when an index is stale. Use `cfind --index` only when an immediate refresh is needed.
