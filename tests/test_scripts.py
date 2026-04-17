from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO / "scripts" / "bootstrap_logging_structure.py"
REGISTER = REPO / "scripts" / "register_agent_log.py"

sys.path.insert(0, str(REPO / "scripts"))
from register_agent_log import slugify  # noqa: E402


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def test_bootstrap_creates_structure(tmp_path: Path) -> None:
    run(BOOTSTRAP, "--root", str(tmp_path))
    assert (tmp_path / "docs" / "code-base-ai-update-logs.md").exists()
    assert (tmp_path / "docs" / "agent-execution-registry.md").exists()
    assert (tmp_path / "docs" / "agent-logs").is_dir()


def test_bootstrap_is_idempotent(tmp_path: Path) -> None:
    run(BOOTSTRAP, "--root", str(tmp_path))
    central = tmp_path / "docs" / "code-base-ai-update-logs.md"
    central.write_text("custom content")
    run(BOOTSTRAP, "--root", str(tmp_path))
    assert central.read_text() == "custom content"


def test_register_produces_expected_id(tmp_path: Path) -> None:
    run(BOOTSTRAP, "--root", str(tmp_path))
    result = run(
        REGISTER,
        "--root", str(tmp_path),
        "--agent-label", "Claude Opus 4.7",
        "--tool-family", "Claude Code",
        "--model", "Opus 4.7",
    )
    assert "registered=claude-code-opus-4-7" in result.stdout
    log = tmp_path / "docs" / "agent-logs" / "claude-code-opus-4-7.md"
    assert log.exists()


def test_register_is_idempotent(tmp_path: Path) -> None:
    run(BOOTSTRAP, "--root", str(tmp_path))
    args = [
        "--root", str(tmp_path),
        "--agent-label", "Claude Opus 4.7",
        "--tool-family", "Claude Code",
        "--model", "Opus 4.7",
    ]
    run(REGISTER, *args)
    run(REGISTER, *args)
    registry = (tmp_path / "docs" / "agent-execution-registry.md").read_text()
    assert registry.count("`claude-code-opus-4-7`") == 1


def test_register_label_drift_no_duplicate(tmp_path: Path) -> None:
    run(BOOTSTRAP, "--root", str(tmp_path))
    run(
        REGISTER,
        "--root", str(tmp_path),
        "--agent-label", "Claude Opus 4.7",
        "--agent-id", "claude-code-opus-4-7",
    )
    run(
        REGISTER,
        "--root", str(tmp_path),
        "--agent-label", "Claude Opus 4.7 ",
        "--agent-id", "claude-code-opus-4-7",
    )
    registry = (tmp_path / "docs" / "agent-execution-registry.md").read_text()
    assert registry.count("`claude-code-opus-4-7`") == 1


def test_slugify_edge_cases() -> None:
    assert slugify("") == "unknown-agent"
    assert slugify("   ") == "unknown-agent"
    assert slugify("Claude Code") == "claude-code"
    assert slugify("  Claude   Code!!  ") == "claude-code"
    assert slugify("GPT-5.4") == "gpt-5-4"
