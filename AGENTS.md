# Repository Instructions

When committing changes, bump these release versions together and keep them identical:

- `package.json`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

For skills:

- Keep invoke-only controls in sync: `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; add or remove both together.
- Do not create `agents/openai.yaml` unless provider-specific behavior requires it. Keep skill files minimal.
- Keep descriptions short and specific: include only enough context for an agent to decide whether to invoke the skill.
