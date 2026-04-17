# Integration Snippets

Use these snippets when adopting the skill in a repository or agent runtime.

## Recommended Repo Structure

- `docs/code-base-ai-update-logs.md`
- `docs/agent-execution-registry.md`
- `docs/agent-logs/<agent-id>.md`

## One-Time Bootstrap

Run:

```bash
python3 scripts/bootstrap_logging_structure.py --root /path/to/repo
```

Then add one instruction snippet to each agent surface you actually use.

For the exact log entry format, see the "Central Log Format" and
"Per-Agent Log Format" sections in [`SKILL.md`](../SKILL.md).

## Generic Instruction Snippet

```md
Every AI-written code change must be logged before the task is complete.

Required:
1. Append a dated entry to `docs/code-base-ai-update-logs.md`.
2. If this repo uses per-agent logs, append/update the current agent file in
   `docs/agent-logs/`.
3. If the current agent file does not exist yet, register it in
   `docs/agent-execution-registry.md`.
4. Update instruction and plan docs when they would otherwise be wrong.
```

## AGENTS.md / AGENT.md / CLAUDE.md Snippet

```md
This repo keeps:
- a mandatory central AI log at `docs/code-base-ai-update-logs.md`
- per-agent logs tracked in `docs/agent-execution-registry.md`

If you are a new AI agent or model variant, register your per-agent log before
or alongside your first write task.
```

## Cursor Rule Snippet

```md
---
description: Require central and per-agent AI logging for every code change
alwaysApply: true
---

Every code change made by an AI agent must be logged before the task is
considered complete.

Required:
- Append `docs/code-base-ai-update-logs.md`
- If `docs/agent-execution-registry.md` exists, append/update the current
  agent file under `docs/agent-logs/`
- Register new agent/model files before completing the task
```

## Register a New Agent

```bash
python3 scripts/register_agent_log.py \
  --root /path/to/repo \
  --agent-label "Claude Opus 4.7" \
  --tool-family "Claude Code" \
  --model "Opus 4.7"
```

## Codex Install

Place this folder at:

- `$CODEX_HOME/skills/agent-execution-logging`
- or `~/.codex/skills/agent-execution-logging`

## Non-Codex Use

Other agents can still use the same contract:

- copy the snippets above into their rule or instruction system
- use the same `docs/` structure
- use the same registration script
