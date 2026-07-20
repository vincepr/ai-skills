# Testing Anti-Patterns

Use this reference when writing or changing tests, adding mocks, or considering production APIs that exist only for tests.

Core rule: tests verify real observable behavior. Test doubles help isolate boundaries; they are not the behavior under test.

## Testing the Mock

Bad tests assert that a mocked component rendered, a stub was called, or a fake value exists without proving the real behavior expected from the subject.

Before asserting on a mock, ask:

- What user-visible or caller-visible behavior does this assertion prove?
- Would the test still provide value if the mock implementation changed?
- Can the real collaborator be used instead?

If the assertion only proves that the mock works, remove it or test through a real boundary.

Interaction assertions are appropriate when the interaction itself is the contract, such as publishing a command or refusing a dangerous call. Assert the meaningful arguments and outcome, not incidental call structure.

## Test-Only Production APIs

Do not add methods, branches, or visibility to production code solely to make test setup or cleanup convenient.

Before changing a production API, ask:

- Is this capability needed by production callers?
- Does this type actually own the resource or lifecycle being exposed?
- Could a fixture, helper, or test harness perform the operation instead?

Keep test-only lifecycle and cleanup logic in test utilities unless it represents a real production responsibility.

## Mocking Without Understanding

A high-level mock can remove side effects that the behavior under test depends on, producing false failures or false confidence.

Before mocking a dependency:

1. Understand what the real dependency reads, writes, returns, and triggers.
2. Determine which of those effects the test requires.
3. Mock the lowest slow, nondeterministic, destructive, or external boundary that preserves required behavior.
4. If uncertain, run with the real implementation first and observe what is actually needed.

Never mock something merely "to be safe."

## Inaccurate Test Doubles

Mocks, fakes, and fixtures must honor the real contract:

- required fields and valid combinations
- relevant side effects
- error behavior
- ordering or lifecycle constraints

Use actual schemas, examples, or implementations to build the double. Include all structurally or behaviorally relevant data, not only the fields used by the first assertion.

Prefer contract tests or shared fixture builders when many tests depend on the same external shape.

## Excessive Mocking

Warning signs:

- setup is longer than the behavior being tested
- most collaborators must be mocked
- tests break whenever implementation details move
- the fake is becoming a second implementation
- the need for a mock cannot be explained

Respond by reconsidering the test level, reducing coupling, or using a focused integration test with real components.

## Tests Added Afterward

Tests are part of implementation, not a later verification phase. For new behavior, observe a meaningful failure before writing production code. A test that passes immediately may add coverage, but it does not establish a test-driven cycle.

## Quick Check

Before accepting a test involving doubles, confirm:

- it proves behavior rather than mock existence
- no production API was added only for the test
- mocked side effects are understood
- the double matches the real contract
- an integration test would not be simpler and more trustworthy
