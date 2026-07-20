---
name: using-git-worktrees
description: Use when starting feature or implementation work that needs isolation from the current checkout, or before executing a plan in a separate worktree.
---

# Using Git Worktrees

Keep task changes isolated without disturbing the current checkout.

Core order: detect existing isolation, use environment-managed isolation when available, then fall back to a manual Git worktree.

## 1. Detect Existing Isolation

Before creating anything, resolve the repository's Git directory and common Git directory:

```bash
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 1
git_dir=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
git_common=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
branch=$(git branch --show-current)
superproject=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
```

If the repository root cannot be resolved, stop: a Git worktree cannot be created from the current context. Use `repo_root` for all project-relative checks and manual worktree commands below.

If `git_dir` and `git_common` differ and `superproject` is empty, the checkout is already a linked worktree. Use it; do not create a nested worktree.

Report whether it is on a named branch or detached HEAD. Do not silently create a branch in an externally managed detached workspace.

Treat a submodule as a normal checkout for this decision rather than mistaking it for an isolated task worktree.

## 2. Confirm Isolation Is Wanted

If the user or project instructions already require an isolated workspace, proceed. Otherwise ask once before creating one. If isolation is declined, work in place and continue with setup and baseline verification.

Do not create a worktree merely because this skill was loaded.

## 3. Prefer Managed Isolation

If the execution environment provides managed workspace or worktree creation, use it. Managed isolation may control directory placement, branch lifecycle, cleanup, permissions, and session state.

Do not create parallel manual Git state that the environment cannot track. Use the manual fallback only when managed isolation is unavailable.

## 4. Select a Manual Worktree Location

Follow this priority:

1. explicit user or project preference
2. existing `.worktrees/` directory
3. existing `worktrees/` directory
4. `.worktrees/` at the repository root

If both conventional directories exist, prefer `.worktrees/` unless project instructions say otherwise.

For a project-local directory, keep its repository-relative path in `location_rel`, derive its absolute path in `location`, and verify that specific directory is ignored. The trailing slash allows directory-only ignore rules to match before the directory exists:

```bash
location="$repo_root/$location_rel"
git -C "$repo_root" check-ignore -q --no-index -- "$location_rel/"
```

If the selected directory is not ignored, add the appropriate ignore rule through the project's normal change and approval workflow before proceeding. This prevents worktree contents from appearing as repository files.

Choose a short task-specific branch name. Verify that neither the target branch nor target directory would be overwritten.

## 5. Create the Manual Worktree

Run the Git operation against the repository root. `location` may be an absolute external directory or the absolute form of the selected project-local directory:

```bash
path="$location/$branch_name"
git -C "$repo_root" worktree add "$path" -b "$branch_name"
```

Then perform all task work from the new checkout. Verify its absolute path, branch or detached state, and clean status before making changes.

If creation fails, diagnose the error. Do not delete Git metadata, overwrite a directory, switch locations silently, or fall back to working in place without informing the user.

## 6. Establish a Baseline

- Follow the project's documented setup process.
- Restore dependencies only when needed.
- Run the relevant tests or checks before implementation.
- Record the command and result.

If the baseline fails, report the failures and ask whether to investigate them or proceed with them documented as pre-existing. Do not silently build new work on an unexplained failing baseline.

## Report

Before implementation, report:

- worktree path
- branch or detached state
- whether isolation is managed or manual
- setup performed
- baseline result

Do not remove a manual worktree or branch unless cleanup is requested. For managed isolation, let the environment own its lifecycle.

Never discard, reset, commit, or modify unrelated work in the original checkout while setting up isolation.
