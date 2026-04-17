---
name: agent-execution-logging
description: Use this skill when a repository needs consistent AI execution logs across Codex, Cursor, Claude Code, Claude CLI, or other agent environments. It standardizes a mandatory central change log, optional per-agent logs, and a lightweight registration flow for new agent or model identities.
---

# Agent Execution Logging

Use this skill when the user wants every AI agent that edits a repository to
leave a clear, repeatable execution trail.

## What This Skill Solves

- Multiple AI tools touch the same repo
- Different model variants need a shared logging contract
- Teams want one central AI change log plus optional per-agent logs
- New agent or model identities should be added without hand-editing multiple
  instruction files every time

## Default Layout

If the repo does not already define a logging structure, use:

- Central log: `docs/code-base-ai-update-logs.md`
- Agent registry: `docs/agent-execution-registry.md`
- Per-agent logs: `docs/agent-logs/<agent-id>.md`

If the repo already has an equivalent structure, follow the repo's existing
contract instead of forcing these defaults.

## Workflow

### 1. Discover the repo contract

Read the instruction surface first:

- `AGENTS.md`
- `AGENT.md`
- `CLAUDE.md`
- Cursor rule files under `.cursor/rules/`

Resolve:

- whether a central log already exists
- whether per-agent logs are enabled
- whether the repo already names specific agent or model files

### 2. Resolve the current agent identity

Prefer, in this order:

1. User-provided agent label
2. Repo-defined label
3. Tool family plus model name
4. Safe fallback slug

Stable examples (match what `register_agent_log.py` emits when both
`--tool-family` and `--model` are passed):

- `cursor-composer-2-0`
- `claude-code-opus-4-7`
- `codex-gpt-5-4`

### 3. Bootstrap the repo if needed

If the repo has no central log or registry yet, run:

`scripts/bootstrap_logging_structure.py`

That creates the default `docs/` logging structure. It does not rewrite the
repo's instruction files for you; use the integration snippets in
`references/integration-snippets.md` for that one-time setup.

### 4. Register new agents when needed

If the repo uses per-agent logs and the current agent is missing from the
registry, run:

`scripts/register_agent_log.py`

This creates the per-agent file and adds the registry row.

### 5. Log before closing any write task

For any task that edits files:

- append a dated entry to the central log
- append a matching entry to the per-agent log if the repo uses one
- update instruction or plan docs that would otherwise become misleading

Read-only exploration does not require log entries.

## Central Log Format

Use the repo's existing format when present. Otherwise use:

```md
## YYYY-MM-DD — Short Title

**What changed:** 1-3 short sentences.

**Files touched:**
- `path/to/file` — what changed
- `path/to/other` — what changed

**Follow-ups:** optional
```

## Per-Agent Log Format

Use:

```md
## YYYY-MM-DD — Short Title

**Task:** 1-2 short sentences.

**Files touched:**
- `path/to/file` — what changed

**Central log:** `docs/code-base-ai-update-logs.md`

**Notes:** optional
```

## Resources

- Read `references/integration-snippets.md` for AGENTS/CLAUDE/Cursor setup
  text.
- Run `scripts/bootstrap_logging_structure.py` to scaffold the default docs
  layout in a repo.
- Run `scripts/register_agent_log.py` to add a new per-agent log file and
  registry entry.

## Guardrails

- Never treat logging as optional for code edits.
- Never replace the central log with per-agent files.
- Never keep a manual list of model files in multiple instruction documents if
  a single registry file can own that mapping.
- Keep entries short, concrete, and file-referenced.
