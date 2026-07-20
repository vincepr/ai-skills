---
name: systematic-debugging
description: Use when encountering a bug, test failure, build failure, performance problem, or unexpected behavior, before proposing a fix.
---

# Systematic Debugging

Random changes hide evidence and create new failures. Find the root cause before changing production behavior.

<HARD-GATE>
Do not propose or implement a fix until the root-cause investigation has produced evidence explaining what fails, where it first fails, and why.
</HARD-GATE>

Use this process especially when a quick fix seems obvious, time pressure is high, earlier attempts failed, or a dependency is not fully understood.

## Phase 1: Root-Cause Investigation

### Read the Evidence

- Read complete errors, warnings, stack traces, and relevant logs.
- Record exact file names, locations, error codes, inputs, and environment details.
- Do not skip an earlier warning because a later error looks more important.

### Reproduce the Failure

- Find the smallest reliable reproduction.
- Record exact steps, inputs, and conditions.
- Determine whether it fails consistently or only under particular timing, order, load, or environment.
- If it is not reproducible, gather more evidence rather than guessing.

### Check What Changed

Inspect relevant diffs, recent commits, dependency changes, configuration changes, persisted state, and environmental differences. Treat correlation as a lead, not proof.

### Locate the First Bad Boundary

For systems with multiple components, instrument each boundary and run once to determine where correct state first becomes incorrect.

At each boundary, observe:

- data entering
- data leaving
- configuration and environment propagation
- local state and side effects

Then narrow the investigation to the first failing component. Do not patch the last component that reports the damage.

### Trace Backward

When the symptom is deep in a call chain, trace values and callers backward until reaching the original trigger. See [root-cause-tracing.md](root-cause-tracing.md).

## Phase 2: Pattern Analysis

Before fixing:

1. Find a similar working path in the same codebase.
2. If following a reference implementation, read it completely rather than copying a fragment.
3. List every observed difference between working and failing cases before deciding which differences matter.
4. Identify required dependencies, configuration, environment, state, ordering, and hidden assumptions.

The goal is to explain why one case works and the other does not.

## Phase 3: Hypothesis and Experiment

State one falsifiable hypothesis:

> I think X is the root cause because Y. If true, experiment Z should produce result R.

Then:

- test one variable at a time
- use the smallest reversible experiment
- predict the result before running it
- distinguish diagnostic changes from production fixes
- record whether the result confirms or rejects the hypothesis

If rejected, remove the experimental change when safe, return to the evidence, and form a new hypothesis. Do not stack guesses.

If something is not understood, say so and investigate it. Confidence is not evidence.

## Phase 4: Fix and Verify

After the root cause is confirmed:

1. Add the smallest automated regression test, or a focused reproduction script when no test framework exists. If `test-driven-development` is available, use its complete red-green-refactor workflow.
2. Verify that it fails for the expected reason.
3. Make one focused change that addresses the root cause.
4. Verify the regression test, original reproduction, and relevant broader checks.
5. Remove temporary diagnostics unless they provide useful ongoing observability.
6. Consider proportionate validation at boundaries that could otherwise admit the same invalid state. See [defense-in-depth.md](defense-in-depth.md).

For flaky async failures, replace guessed delays with observable conditions. See [condition-based-waiting.md](condition-based-waiting.md).

## Failed-Fix Gate

Count attempted fixes.

- After one or two failed fixes, return to Phase 1 with the new evidence.
- After three failed fixes, stop attempting patches.
- Do not attempt a fourth fix before discussing whether the architecture, shared state, or coupling is the real problem.

Architecture is suspect when each fix exposes a different coupled failure, requires broad refactoring merely to test, or creates new symptoms elsewhere.

## Stop Signals

Return to Phase 1 if you catch yourself:

- trying one quick change before investigating
- bundling several possible fixes into one test run
- proposing a solution before tracing the data
- keeping a failed fix while adding another
- weakening or skipping the regression test
- claiming a dependency is irrelevant without reading it
- treating a visible symptom as the cause

## External or Timing-Dependent Causes

If evidence shows the cause is environmental, timing-dependent, or external:

1. Document what was investigated and what evidence isolates the external cause.
2. Add appropriate handling such as a timeout, retry, fallback, or actionable error.
3. Add observability that will make a future occurrence diagnosable.
4. Verify the behavior under both success and failure conditions.

## Completion

Debugging is complete only when the root cause is explained, the fix addresses that cause, the original failure no longer reproduces, and relevant checks pass without unexplained output.
