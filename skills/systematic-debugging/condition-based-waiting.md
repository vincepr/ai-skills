# Condition-Based Waiting

Use when asynchronous tests or workflows rely on guessed delays, fail under load, or time out when run concurrently.

Core rule: wait for the observable condition that matters, not an estimate of how long the operation should take.

## Replace Delays with Conditions

Wait for fresh observable state such as:

- an event with a specific type or payload
- a state transition
- an expected item count
- a file or resource becoming available
- a predicate over multiple values

Check the state again on every iteration. Do not cache it before waiting.

## Generic Pattern

```text
deadline = now + timeout

loop:
  result = observe_current_state()
  if desired_condition(result):
    return result

  if now >= deadline:
    fail with the condition, timeout, and last observed state

  wait for a short polling interval or the next relevant event
```

Prefer event notification when the system exposes it. Otherwise use a polling interval that is responsive without creating unnecessary load.

Always include a timeout. A failed wait should explain what condition was expected and what was last observed.

## Common Mistakes

- Polling so quickly that the test creates load or starvation.
- Omitting a timeout and hanging forever.
- Reusing stale state inside the loop.
- Waiting for an indirect signal when the real condition is observable.
- Increasing the delay whenever CI is slower.

## When a Fixed Delay Is Correct

A fixed duration is appropriate only when elapsed time is itself the behavior under test, such as debounce, throttle, lease, or retry timing.

In that case:

1. First wait for the event that starts the timed behavior.
2. Derive the delay from a known configured interval, not a guess.
3. Document why that duration is required.
4. Allow reasonable scheduling tolerance without making the assertion meaningless.
