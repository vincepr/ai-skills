# ai-skills

Provider-independent workflows for planning, engineering, and collaboration using the [Agent Skills](https://agentskills.io) format.

- `api-grafana`
- `brainstorming`
- `code-find`
- `code-review`
- `dotnet-dump-debug`
- `dotnet-swap-package-to-local-project`
- `grill-me`
- `handoff`
- `review-gate`
- `systematic-debugging`
- `test-driven-development`
- `using-git-worktrees`

## Claude Code

```text
/plugin marketplace add vincepr/ai-skills
/plugin install ai-skills@ai-skills
/reload-plugins
```

Install one skill instead with, for example, `/plugin install systematic-debugging@ai-skills`.

## Codex

```text
codex plugin marketplace add vincepr/ai-skills
codex plugin add ai-skills@ai-skills
```

Start a new session after installation. For one skill, ask `$skill-installer` to install that skill's directory from `vincepr/ai-skills`.

## OpenCode

Add the git-backed plugin to `opencode.json`, then restart OpenCode:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["ai-skills@git+https://github.com/vincepr/ai-skills.git"]
}
```

OpenCode caches git-backed plugins. A repository version bump does not refresh an existing cached install; change the configured spec to a new tag or clear the cached package.

Alternatively, clone the repository and add its `skills/` directory to `skills.paths`:

```text
git clone https://github.com/vincepr/ai-skills.git ~/.local/share/ai-skills
```

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/.local/share/ai-skills/skills"]
  }
}
```

## Cross-Client Installer

The third-party [skills CLI](https://skills.sh) can install all or selected skills:

```text
npx skills add vincepr/ai-skills
```

MIT licensed. Adapted from [obra/superpowers](https://github.com/obra/superpowers).
