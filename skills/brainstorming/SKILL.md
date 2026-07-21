---
name: brainstorming
description: Use before creating features, components, APIs, workflows, or architecture, or modifying existing behavior.
disable-model-invocation: true
---

# Brainstorming

Turn an idea into an approved design and written specification through collaborative dialogue.

<HARD-GATE>
Do not write code, scaffold a project, or begin implementation during this workflow. Finish only after the written specification has passed review, the user has approved it, and the work has been handed off to planning. This applies even when the task appears simple; simple tasks get short designs, not no design.
</HARD-GATE>

## Workflow

Complete these stages in order:

1. Explore the project context.
2. Check whether the scope must be decomposed.
3. Clarify intent, constraints, and success criteria.
4. Compare two or three viable approaches.
5. Present the design and obtain approval.
6. Write the approved design as a specification.
7. Review the written specification.
8. Ask the user to review and approve the specification.
9. Move to implementation planning.

Track these stages explicitly when the work is substantial.

## Explore Context

Inspect the relevant code, documentation, conventions, and recent changes before asking detailed questions. Understand what already exists and where the proposed work fits.

Do not ask the user for information that is readily available in the project.

## Check Scope

Before refining details, determine whether the request contains multiple independent subsystems.

If it does, first agree on:

- the separate units of work
- how they relate
- their implementation order
- which unit to design now

Each independently useful subsystem should receive its own specification, plan, and implementation cycle. Do not force a platform-sized request into one design.

## Clarify the Idea

Ask questions one at a time. Prefer concrete choices when they make the decision easier, while allowing an open answer when the options are not known.

Establish:

- the problem and desired outcome
- users or callers affected
- constraints and compatibility requirements
- success criteria
- explicit non-goals
- important edge cases

Focus on decisions that can materially change the design. Do not interrogate the user about inconsequential details.

## Compare Approaches

Offer two or three genuinely different approaches when meaningful. For each, explain the important trade-offs: complexity, coupling, extensibility, migration cost, operational risk, and fit with the existing system.

Lead with the recommended approach and explain why it best fits the stated goals. Apply YAGNI: do not add capabilities that were not requested and are not needed by the design.

## Present the Design

Scale the design to the task. A simple change may need a few sentences; a complex design may need several short sections. For complex work, validate each section before continuing.

Cover what is relevant:

- architecture and affected components
- responsibilities and interfaces
- data and control flow
- state and lifecycle
- failure handling and edge cases
- compatibility or migration
- testing and verification

### Design for Clear Boundaries

Break the system into smaller units that each:

- have one clear purpose
- communicate through well-defined interfaces
- can be understood and tested independently
- state what they do, how they are used, and what they depend on

A caller should not need to read a unit's internals to use it correctly. Its internals should be changeable without breaking callers. If that is not true, improve the boundary.

Prefer focused files and components that fit in working context. A file that keeps growing is often carrying more than one responsibility.

### Existing Codebases

Follow established project patterns unless changing them is necessary for the goal. If an existing structural problem directly obstructs the work, include a targeted improvement in the design. Do not expand into unrelated refactoring.

## Write the Specification

After conversational approval, write the validated design to the project's preferred specification location. If none exists, use `docs/specs/YYYY-MM-DD-<topic>-design.md`.

The specification should stand on its own and record:

- problem, outcome, and scope
- chosen approach and rejected alternatives
- components, responsibilities, and interfaces
- data flow and failure behavior
- testing strategy
- assumptions and unresolved risks

Follow the project's normal version-control policy. Do not commit solely because this skill was used.

## Review the Specification

Review the written artifact, not just the remembered design. Use [spec-document-reviewer-prompt.md](spec-document-reviewer-prompt.md) for an independent review when possible; otherwise apply the same rubric directly.

Fix blocking issues and repeat the review until it passes. Then ask the user to review the actual specification file. Apply requested changes and review it again.

Do not begin planning until the user approves the written specification.

## Handoff

Once the specification is approved, move to a planning workflow. Planning, not implementation, is the next step.
