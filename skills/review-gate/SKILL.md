---
name: review-gate
description: Take new or existing changes through checks, code review, fixes, and a final local commit.
disable-model-invocation: true
---

# Review Gate

Take an implementation or an existing working tree through a closed review loop:

**implement → check → review → classify → fix → re-check → re-review → commit**

<HARD-GATE>
Do not commit until the exact change has passed relevant project checks and `code-review` reports no open must-fix or should-fix findings. Never push unless the user explicitly requests it.
</HARD-GATE>

## 1. Establish the Scope

Verify that the work is in a Git repository. Record the starting revision, current branch, status, and existing staged, unstaged, and untracked files.

Define the task, specification source, and fixed point for review. Include all files that belong to the task, including relevant untracked files. Preserve unrelated user changes and exclude them from checks, review, staging, and commit where practical. If the task cannot be isolated safely, stop and ask before committing.

Read applicable repository instructions and commit conventions. Do not commit on the default branch unless the user explicitly authorizes it; create an appropriate task branch when the intended name is clear, otherwise ask.

## 2. Implement Without Committing

If implementation is still required, complete it before starting the gate. Use `test-driven-development` when changing production behavior, and stay within the agreed specification.

If changes already exist, treat them as the implementation input. Do not rewrite them merely to claim ownership or add unrelated cleanup.

Do not commit yet.

## 3. Run Project Checks

Discover the relevant build, test, formatting, lint, analysis, and generated-file checks from repository instructions and project configuration.

Run focused checks while fixing issues, then run the relevant broader checks before review. Investigate failures instead of weakening tests, disabling rules, or ignoring unexplained warnings.

Record commands and results. Distinguish confirmed pre-existing failures from failures introduced by the task, but do not silently waive either; an unexplained relevant failure keeps the gate closed.

## 4. Review with `code-review`

Invoke the `code-review` skill against the exact task scope. Supply:

- the fixed point and current revision
- staged, unstaged, and relevant untracked changes
- the originating specification or requirements
- applicable repository standards
- the checks already run and their results

Keep the review local. Do not post comments, update issues, or mutate external systems.

Classify each evidence-backed finding:

- **mustFix** — correctness, security, data-loss, specification, repository-rule, or gate failures that block the commit
- **shouldFix** — concrete maintainability, robustness, or design problems worth addressing now at proportionate effort
- **deferred** — invalid, stale, purely preferential, or genuinely out-of-scope findings, each with a brief reason

Do not defer a blocker or downgrade a finding merely to make the gate pass.

## 5. Fix and Re-review

For every round:

1. Verify each finding against the current code; do not apply stale or incorrect advice blindly.
2. Fix all open `mustFix` and `shouldFix` findings. Use `test-driven-development` for behavior changes.
3. Re-run focused checks and all relevant broader checks.
4. Invoke `code-review` again over the complete updated scope, not only the latest patch.
5. Reclassify findings from current evidence and repeat while actionable findings remain.

The review is clean only when no `mustFix` or `shouldFix` findings remain and no unresolved question could conceal a blocker.

After three unsuccessful rounds on the same issue, stop and report the blocker. Do not force convergence by weakening a check, narrowing the review scope, or relabelling the issue as deferred.

## 6. Final Gate and Commit

Immediately before committing:

1. Confirm all relevant checks are green without unexplained output.
2. Confirm the final `code-review` result is clean for both Standards and Spec, or explicitly records why the Spec axis was unavailable.
3. Inspect status and the complete staged diff.
4. Stage only reviewed task files.
5. Exclude secrets, credentials, local environment files, private data, databases, and generated build output unless explicitly required and safe.
6. Confirm conditional repository requirements triggered by committing, such as synchronized versions or generated metadata, are satisfied.
7. Commit using the repository's message and attribution conventions.

Do not push. Verify the resulting commit and inspect the remaining working tree so unrelated changes are still intact.

## Report

Report:

- commit hash and subject
- checks run and final results
- review rounds completed
- fixed `mustFix` and `shouldFix` findings
- deferred findings and reasons
- remaining unrelated working-tree changes

If the gate cannot pass, do not commit; report the blocking evidence and the safest next action.
