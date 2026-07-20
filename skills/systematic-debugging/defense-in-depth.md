# Defense-in-Depth Validation

Use after tracing a defect to invalid data or state that can cross more than one trust boundary.

Core rule: fix the source first, then add proportionate safeguards where independent paths could bypass that fix. Repeating the same check everywhere without understanding ownership creates noise, not safety.

## Map the Path

Document:

1. where the invalid state originated
2. each boundary it crossed
3. where the invariant should be established
4. where a bypass would cause irreversible or dangerous effects

## Useful Layers

### Entry Boundary

Reject malformed or obviously invalid external input early with an actionable error.

### Domain Invariant

Validate rules that only business or domain logic understands, even if input shape is valid.

### Dangerous Side Effect

Immediately before filesystem, network, database, deployment, or destructive operations, verify assumptions whose violation could damage the wrong resource or environment.

### Diagnostic Context

For failures that are hard to reproduce, retain structured context that identifies the operation, target, relevant configuration, and caller without leaking secrets.

## Apply Proportionately

Add a safeguard when it:

- protects a distinct boundary or responsibility
- catches an alternate path
- prevents an expensive or irreversible effect
- provides materially better diagnostics

Avoid duplicate checks that cannot catch a different failure or that allow layers to disagree about the invariant.

## Verify the Defense

- Test the source-level fix.
- Attempt an alternate path that bypasses the entry boundary.
- Verify the owning domain layer still rejects invalid state.
- Verify dangerous operations fail safely before side effects occur.
- Confirm errors identify the violated invariant and useful context.
