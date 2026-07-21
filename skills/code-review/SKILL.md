---
name: code-review
description: Review changes since a commit, branch, tag, or merge-base against repository standards and the originating specification.
---

# Code Review

Review a change along two independent axes:

- **Standards** — does the change follow the repository's documented conventions and general design-quality baseline?
- **Spec** — does the change faithfully implement the originating issue, requirement, or specification?

Keep the axes separate so success in one does not hide problems in the other.

<HARD-GATE>
Report only evidence-backed findings introduced by the reviewed change. Do not modify code unless the user asks for fixes.
</HARD-GATE>

## 1. Pin the Review Scope

Use the fixed point supplied by the user: a commit, branch, tag, or other revision. If none was supplied, inspect the branch and upstream configuration for a clear base; ask only when the intended base remains ambiguous.

Resolve the fixed point before reviewing. For committed branch changes, compare `HEAD` with the merge-base using a three-dot diff and inspect the intervening commits. For a work-in-progress review, also include staged, unstaged, and relevant untracked files.

Record the exact commands and paths that define the scope. Stop early if the revision is invalid or the resulting scope is empty.

## 2. Find the Spec

Look for the originating specification in this order:

1. Issue or pull-request references in commit messages or branch metadata.
2. A path or issue supplied by the user.
3. A matching document under common project locations such as `docs/` or `specs/`.
4. Requirements stated directly in the conversation.

Use an available issue-tracker integration when needed. If no specification can be found, ask the user when it is material; otherwise skip the Spec axis and report that no spec was available.

## 3. Find the Standards

Read applicable repository instructions and engineering guidance, including scoped `AGENTS.md` files, contribution guides, coding standards, architectural decisions, and local conventions in the changed area.

Repository guidance overrides the general baseline below. Treat baseline smells as judgement calls, not hard violations, and skip formatting or style issues already enforced by reliable tooling.

## 4. Review Independently

When parallel agents are available and permitted, run the Standards and Spec reviews in separate agents so one does not bias the other. Give each agent the complete review scope, commit list, and only the sources relevant to its axis.

Otherwise perform two clearly separated passes and keep independent notes before aggregating them.

### Standards Pass

Report violations of documented repository guidance with the source and rule. Also inspect the changed code for these language-neutral design smells:

- **Mysterious Name** — a name does not reveal the role or meaning of the code.
- **Duplicated Code** — the same logic or structure is repeated in the change.
- **Feature Envy** — behavior depends more on another object's data than its own.
- **Data Clumps** — the same group of values repeatedly travels together and wants a type.
- **Primitive Obsession** — a primitive value substitutes for a meaningful domain concept.
- **Repeated Branching** — equivalent branching over the same concept appears in several places.
- **Shotgun Surgery** — one logical change requires scattered edits across many locations.
- **Divergent Change** — one module changes for several unrelated reasons.
- **Speculative Generality** — abstractions or extension points exist without a current requirement.
- **Message Chains** — callers navigate deeply through another object's structure.
- **Middle Man** — a type or function mostly delegates without adding responsibility.
- **Refused Bequest** — an implementation inherits a contract or behavior it largely rejects.

Name the smell, explain its concrete impact, and suggest a direction only when the diff provides enough evidence. Do not report a smell merely because the pattern is present.

### Spec Pass

Compare the change with the specification and report:

- required behavior that is missing or partial
- behavior that was not requested and creates meaningful scope or risk
- implemented requirements whose behavior appears incorrect

Cite the relevant requirement for every finding. Do not invent requirements or treat an implementation preference as a specification defect.

## 5. Validate Findings

Before reporting a finding:

1. Read enough surrounding code to understand the changed behavior.
2. Confirm the issue is introduced or exposed by the review scope.
3. Confirm the cited rule applies to the current state; keep obligations triggered by a future action separate from present violations.
4. Check whether tests, tooling, or repository guidance already resolve the concern.
5. State the observable impact rather than only naming a pattern.
6. Include the file and precise location.

Omit uncertain claims that cannot be verified. Surface a question separately when missing context prevents a conclusion.

## 6. Report

Present findings under `## Standards` and `## Spec`. Within each axis, order findings by severity and lead with the problem, impact, and location. Keep the axes separate rather than reranking them into one list.

If an axis has no findings, say so explicitly. If the Spec pass was skipped, state why.

End with the finding count and most severe issue for each axis. Do not choose a single winner across axes.
