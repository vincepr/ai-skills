# Root-Cause Tracing

Use when a failure appears far from the code or input that originally caused it.

Core rule: trace backward through callers and state transitions until the original invalid assumption, value, or event is found. Fixing only the final crash site treats a symptom.

## Process

1. Identify the operation that directly produces the visible failure.
2. Record the bad value or state at that point.
3. Find the caller that supplied it.
4. Record what the caller received, derived, or assumed.
5. Continue upward until reaching the earliest point where correct state became incorrect.
6. Confirm the chain with a focused reproduction or instrumentation.

At each step ask:

- What value was passed?
- Where did it come from?
- Why was it considered valid?
- What ran immediately before it changed?
- Which caller had enough context to reject or prevent it?

## Instrumentation

When static tracing is insufficient, add temporary diagnostics immediately before the dangerous or incorrect operation. Capture enough context to identify the caller and environment:

- arguments and identifiers
- relevant state
- working directory or resource location
- configuration and environment values
- timestamp or event order
- call stack when available

Use an output channel that is visible in the active runtime or test runner. Run the smallest reproduction and remove temporary instrumentation after the cause is confirmed unless it has lasting operational value.

## Test Pollution

When one test leaves state that breaks another:

1. Verify a clean baseline before each candidate run.
2. Run suspected tests individually or in progressively smaller groups.
3. Check for the polluted state immediately after each run.
4. Narrow to the smallest test or sequence that creates it.
5. Trace the side effect to the code that failed to isolate or clean up state.

Use binary search when groups can be divided independently. Otherwise preserve execution order while narrowing, because the bug may require a sequence rather than one test.

Do not rely on a fixed, framework-specific polluter script unless its test command, state check, cleanup, and filename handling match the project.

## Fix Location

Fix the earliest point that owns the violated invariant. Then consider proportionate safeguards at later trust boundaries so alternate paths cannot recreate the same dangerous state.
