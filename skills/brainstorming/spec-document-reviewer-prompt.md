# Spec Document Reviewer Prompt

Use this after a design has been written as a specification. Give the review to an independent reviewer when possible; otherwise apply it directly.

```text
Review the specification at [SPEC_FILE_PATH]. Determine whether it is complete and precise enough to produce one implementation plan.

Check:

1. Completeness
   - TODOs, placeholders, TBDs, or unfinished sections
   - missing behavior, interfaces, failure handling, or verification details that planning depends on

2. Consistency
   - contradictory requirements
   - architecture, component responsibilities, or data flow that disagree across sections

3. Clarity
   - requirements that could reasonably lead to different implementations
   - unstated assumptions or undefined terms that materially affect the design

4. Scope
   - multiple independent subsystems that should have separate specs and plans
   - missing boundaries between units

5. YAGNI
   - unrequested features
   - abstractions or extensibility without a current requirement

Calibrate strictly but practically. Block approval only for issues likely to produce a wrong or incomplete implementation plan. Put wording preferences, minor omissions, and optional improvements under advisory recommendations.

Return exactly:

## Spec Review

**Status:** Approved | Issues Found

**Blocking Issues:**
- [section]: [specific issue] - [why it matters for planning]

**Recommendations:**
- [non-blocking improvement]

Use "None" when a section has no items.
```
