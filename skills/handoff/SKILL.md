---
name: handoff
description: Create a handoff document for continuing work in a fresh session. Use when asked to hand off work or compact context.
---

# Handoff

Write a handoff document summarizing the current conversation so a fresh agent can continue the work. Save it to the temporary directory of the user's operating system, not the current workspace.

Include a "Suggested skills" section listing skills the next agent should invoke.

Do not duplicate content already captured in other artifacts such as specifications, plans, ADRs, issues, commits, or diffs. Reference them by path or URL instead.

Redact sensitive information such as API keys, passwords, and personally identifiable information.

If the user describes what the next session will focus on, tailor the document accordingly.

## What to Include

- **Goal / task** — what the work is trying to accomplish, in one or two sentences.
- **Current state** — what is done, what works, and what has been verified.
- **Next steps** — the concrete, ordered actions the next agent should take.
- **Key context** — decisions and rationale, constraints, gotchas, and dead ends already ruled out.
- **Relevant artifacts** — files touched, branches, merge requests or pull requests, tickets, and documents, referenced by path or URL rather than copied inline.
- **Suggested skills** — skills the next agent should invoke for the work ahead.

## Output Location

Save the file to the OS temporary directory, such as `$TMPDIR` on macOS or `/tmp` on Linux, with a descriptive name like `handoff-<topic>-<date>.md`. Tell the user the full path so they can open it in the next session.
