---
name: test-driven-development
description: Use before changing production code for a feature, bug fix, behavior change, or refactor.
---

# Test-Driven Development

Write the test first. Watch it fail for the expected reason. Write only enough code to pass.

<HARD-GATE>
Do not write new production behavior without first observing a test fail because that behavior is missing or wrong.
</HARD-GATE>

Use TDD for features, bug fixes, and behavior changes. For a pure behavior-preserving refactor, first establish a green test baseline that covers the behavior, then keep it green throughout.

Exceptions such as generated code, declarative configuration, and throwaway prototypes must be explicit and agreed rather than silently treated as TDD.

## If Code Was Written First

If you wrote production implementation before observing a meaningful failing test, remove only your premature implementation and restart from the test.

Do not keep it as a reference, adapt the test around it, or leave it commented out. That biases the test toward what was built instead of what is required.

Never delete or revert pre-existing code, user changes, or unrelated work to enforce this rule.

## Red: Specify One Behavior

1. Choose the smallest next observable behavior.
2. Write one focused test through the public interface.
3. Give it a name that describes the expected behavior.
4. Prefer real code and collaborators; mock only a necessary boundary.
5. Run the test and inspect the failure.

A valid RED state means:

- the test fails, rather than crashing during setup
- the failure message matches the intended missing or incorrect behavior
- the failure is not caused by a typo, broken fixture, or unrelated error

If the test passes immediately, it does not prove the new behavior. Determine whether the behavior already exists or the test does not exercise it.

## Green: Make the Smallest Change

Write the simplest production code that makes the failing test pass.

Do not add speculative options, unrelated cleanup, broad abstractions, or behavior not required by the current test. Run the focused test, then the relevant existing tests.

If a valid test still fails, change production code rather than weakening the requirement encoded by the test.

### Example

For a defect where blank names are accepted:

```text
RED:   submit({ name: " " }) should return "Name required"
RUN:   confirm it fails because no validation result is returned
GREEN: add only the blank-name guard
RUN:   confirm the focused test and relevant suite pass
```

The RED check proves the test detects the defect. The GREEN change does not add unrelated validation or refactoring.

## Refactor: Improve Structure While Green

Only after all relevant tests pass:

- remove duplication
- improve names and boundaries
- simplify implementation and test setup
- extract helpers when they make the design clearer

Do not add behavior during refactoring. Keep tests green, then begin the next cycle with the next failing test.

## Why the Order Matters

A test written after implementation often passes immediately. That cannot show that the test would have caught the missing behavior and tends to encode the implementation rather than the requirement.

Test-first development forces API and edge-case decisions before implementation and proves the test can detect the absence of the behavior.

Manual testing is useful for exploration but is not a repeatable regression check. Record important behavior in automated tests.

## Good Tests

- Test observable behavior, not private implementation details.
- Keep each test focused enough that a failure has one clear meaning.
- Make the test demonstrate the intended API.
- Cover important error paths and boundaries, not only the happy path.
- Use real collaborators when practical.
- When mocking, preserve the real contract and required side effects.

Read [testing-anti-patterns.md](testing-anti-patterns.md) when changing tests, introducing mocks, or considering test-only production APIs.

## Existing and Exploratory Code

Exploration can clarify an unfamiliar API or design. Keep it disposable. Once the direction is understood, discard the exploratory implementation and begin the production change from RED.

For legacy code without coverage, add a characterization test around the behavior being changed. Do not require unrelated legacy code to be retrofitted first.

For a defect, confirm the root cause before applying TDD to the fix. If that investigation has not already happened, use `systematic-debugging` when available; otherwise reproduce the issue, trace the failing data or state to its source, and test one hypothesis at a time. Then write a regression test for the confirmed failure before applying the fix.

## When Testing Is Difficult

Treat testing difficulty as design feedback:

| Problem | Response |
|---|---|
| The API is unclear | Write the wished-for call and assertion first. |
| The test is complicated | Simplify the public interface or responsibilities. |
| Everything must be mocked | Reduce coupling or inject the boundary. |
| Setup dominates the test | Extract fixtures; if still large, reconsider the design. |
| Mocks are more complex than real collaborators | Prefer a focused integration test. |

## Completion Checklist

- Every changed behavior was driven by a meaningful RED state.
- Each RED failure occurred for the expected reason.
- Production changes were the minimum needed for GREEN.
- Refactoring happened only while tests were green.
- Focused and relevant broader tests pass.
- Test output has no unexplained errors or warnings.
- Important errors and edge cases are covered.

If the test never failed first, the work may be tested, but it was not test-driven.
