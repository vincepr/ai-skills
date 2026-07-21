---
name: test-driven-development
description: Use before changing production code for a feature, bug fix, behavior change, or refactor.
---

# Test-Driven Development

Work in vertical slices: specify one observable behavior, watch its test fail for the expected reason, write only enough code to pass, then improve the design while green.

<HARD-GATE>
Do not write new production behavior without first observing a test fail because that behavior is missing or wrong.
</HARD-GATE>

Use TDD for features, bug fixes, and behavior changes. For a behavior-preserving refactor, first establish a green test baseline that covers the behavior, then keep it green.

Follow the project's test conventions, architectural decisions, and domain vocabulary. Make exceptions such as generated code, declarative configuration, and throwaway prototypes explicit and get user agreement.

## If Code Was Written First

If you wrote production implementation before observing a meaningful failing test, remove only your premature implementation and restart from the test. Do not retain it as a reference, adapt the test around it, or leave it commented out; that biases the test toward what was built rather than what is required.

Never delete or revert pre-existing code, user changes, or unrelated work to enforce this rule.

## Red: Specify One Behavior

1. Choose the smallest next observable behavior.
2. Choose the public boundary where that behavior can be observed.
3. Write one focused test with a name that describes the expected behavior.
4. Derive the expected result independently from the code under test, using the requirement, specification, or a worked example.
5. Prefer real code and collaborators; mock only a necessary boundary.
6. Run the test and inspect the failure.

A valid RED state means:

- the test fails rather than crashing during setup
- the failure matches the intended missing or incorrect behavior
- the failure is not caused by a typo, broken fixture, or unrelated error

If the test passes immediately, determine whether the behavior already exists or the test does not exercise it. A passing test cannot prove that it detects the missing behavior.

Complete this test-to-implementation cycle before specifying the next behavior. Do not write a batch of tests for imagined future behavior.

## Green: Make the Smallest Change

Write the simplest production code that makes the failing test pass. Do not add speculative options, unrelated cleanup, broad abstractions, or behavior not required by the current test.

Run the focused test, then the relevant existing tests. If a valid test still fails, change production code rather than weakening the requirement encoded by the test.

## Refactor: Improve Structure While Green

Only after all relevant tests pass, remove duplication, improve names and boundaries, simplify implementation and test setup, and extract helpers when they clarify the design.

Do not add behavior during refactoring. Keep tests green, then start the next cycle with the next failing test.

## Test Quality

- Test observable behavior through public interfaces, not private implementation details.
- Keep each test focused enough that a failure has one clear meaning.
- Make the test demonstrate the intended API.
- Cover important error paths and boundaries, not only the happy path.
- Do not recompute expected values with the implementation's algorithm.
- When mocking, preserve the real contract and required side effects.

Read [testing-anti-patterns.md](testing-anti-patterns.md) when changing tests, introducing mocks, or considering test-only production APIs.

## Existing and Exploratory Code

Keep exploratory implementation disposable. Once the direction is understood, discard it and begin the production change from RED.

For legacy code without coverage, add a characterization test around the behavior being changed; do not require unrelated legacy code to be retrofitted first.

For a defect, confirm the root cause before applying TDD. Use `systematic-debugging` when available; otherwise reproduce the issue, trace it to its source, and test one hypothesis at a time. Then write a regression test for the confirmed failure before fixing it.

## When Testing Is Difficult

Treat testing difficulty as design feedback:

| Problem | Response |
|---|---|
| The API is unclear | Write the wished-for call and assertion first. |
| The test is complicated | Simplify the public interface or responsibilities. |
| Everything must be mocked | Reduce coupling or inject the boundary. |
| Setup dominates the test | Extract fixtures; if still large, reconsider the design. |
| Mocks exceed real collaborators in complexity | Prefer a focused integration test. |

## Completion Check

- Every changed behavior was driven by a meaningful RED state.
- Production changes were the minimum needed for GREEN.
- Refactoring happened only while relevant tests were green.
- Focused and relevant broader tests pass without unexplained errors or warnings.
- Important error paths and boundaries are covered.

If the test never failed first, the work may be tested, but it was not test-driven.
