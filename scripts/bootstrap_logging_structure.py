#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


CENTRAL_LOG_CONTENT = """# Codebase AI update logs

Running log of AI-assisted changes to this repository. Append new entries here
instead of creating one-off markdown files.
"""


REGISTRY_CONTENT = """# Agent Execution Registry

This registry tracks per-agent execution logs. The central change log at
`docs/code-base-ai-update-logs.md` remains mandatory for every AI-written code
change.

## Registered Agents

| Agent | ID | Log file | Notes |
| --- | --- | --- | --- |
"""


def ensure_file(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the default AI execution logging structure in a repo."
    )
    parser.add_argument("--root", default=".", help="Repo root. Defaults to cwd.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    docs_dir = root / "docs"
    agent_logs_dir = docs_dir / "agent-logs"

    docs_dir.mkdir(parents=True, exist_ok=True)
    agent_logs_dir.mkdir(parents=True, exist_ok=True)

    ensure_file(docs_dir / "code-base-ai-update-logs.md", CENTRAL_LOG_CONTENT)
    ensure_file(docs_dir / "agent-execution-registry.md", REGISTRY_CONTENT)

    print(f"central_log={docs_dir / 'code-base-ai-update-logs.md'}")
    print(f"registry={docs_dir / 'agent-execution-registry.md'}")
    print(f"agent_logs_dir={agent_logs_dir}")


if __name__ == "__main__":
    main()
