# Agent Execution Logging

A reusable skill and helper-script bundle for enforcing AI execution logging
across repositories touched by multiple agents, tools, or model variants.

It is designed for teams using combinations of:

- Codex
- Cursor
- Claude Code
- Claude CLI
- other agent frameworks with instruction or rule files

The goal is simple:

- keep one mandatory central AI change log
- optionally keep per-agent logs
- register new agent/model identities without manually editing multiple docs

## What You Get

- `SKILL.md`
  The actual skill definition for Codex-style skill loading.
- `agents/openai.yaml`
  UI metadata for Codex skill discovery.
- `references/integration-snippets.md`
  Ready-to-paste snippets for `AGENTS.md`, `AGENT.md`, `CLAUDE.md`, and Cursor
  rules.
- `scripts/bootstrap_logging_structure.py`
  Creates the default `docs/` logging structure in any repo.
- `scripts/register_agent_log.py`
  Registers a new agent/model log file and updates the registry.

## Default Logging Structure

When a repo does not already have its own structure, this package uses:

```text
docs/
  code-base-ai-update-logs.md
  agent-execution-registry.md
  agent-logs/
    <agent-id>.md
```

## Install

### Codex skill install

Clone or copy this repo, then place the folder at one of:

```bash
$CODEX_HOME/skills/agent-execution-logging
```

or:

```bash
~/.codex/skills/agent-execution-logging
```

### Generic local install

If you do not use Codex skills directly, keep this repo anywhere you want and
run the helper scripts from it.

Example:

```bash
git clone https://github.com/<your-org>/agent-execution-logging.git
cd agent-execution-logging
```

## Quick Start

### 1. Bootstrap a target repo

```bash
python3 scripts/bootstrap_logging_structure.py --root /path/to/target-repo
```

This creates:

- `docs/code-base-ai-update-logs.md`
- `docs/agent-execution-registry.md`
- `docs/agent-logs/`

### 2. Register an agent/model

```bash
python3 scripts/register_agent_log.py \
  --root /path/to/target-repo \
  --agent-label "Claude Opus 4.7" \
  --tool-family "Claude Code" \
  --model "Opus 4.7"
```

Example output:

```text
registered=claude-code-opus-4-7
registry=/path/to/target-repo/docs/agent-execution-registry.md
log_file=/path/to/target-repo/docs/agent-logs/claude-code-opus-4-7.md
```

### 3. Add the rule text to your agents

Use the snippets in:

[`references/integration-snippets.md`](./references/integration-snippets.md)

## Typical Workflow

1. Install the skill or keep this repo locally.
2. Bootstrap a target repository once.
3. Add the instruction snippets to the agent surfaces you use.
4. Register each new agent/model once.
5. Require central log updates for every AI-written code change.

## Example Usage

### Codex

Ask:

```text
Use $agent-execution-logging to set up consistent AI logging for this repo.
```

### Cursor / Claude / other agents

Paste the snippets from
[`references/integration-snippets.md`](./references/integration-snippets.md)
into the repo's instruction files or rule system.

## Notes

- This package does not force a repo to use the default structure if it already
  has a good equivalent.
- The central log should remain mandatory even if per-agent logs are optional.
- The registry exists to avoid maintaining duplicated model lists across
  multiple instruction files.

## License

[MIT](./LICENSE)
