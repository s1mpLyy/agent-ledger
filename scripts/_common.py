from __future__ import annotations

REGISTRY_TEMPLATE = """# Agent Execution Registry

This registry tracks per-agent execution logs. The central change log at
`docs/code-base-ai-update-logs.md` remains mandatory for every AI-written code
change.

## Registered Agents

| Agent | ID | Log file | Notes |
| --- | --- | --- | --- |
"""


CENTRAL_LOG_TEMPLATE = """# Codebase AI update logs

Running log of AI-assisted changes to this repository. Append new entries here
instead of creating one-off markdown files.

<!-- Entry Template

## YYYY-MM-DD — Short Title

**What changed:** 1-3 short sentences.

**Files touched:**
- `path/to/file` — what changed
- `path/to/other` — what changed

**Follow-ups:** optional

-->
"""
