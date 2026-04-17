#!/usr/bin/env node
"use strict";

const { execFileSync } = require("child_process");
const path = require("path");

const SCRIPTS = path.resolve(__dirname, "..", "scripts");
const REFS = path.resolve(__dirname, "..", "references");

const COMMANDS = {
  bootstrap: path.join(SCRIPTS, "bootstrap_logging_structure.py"),
  register: path.join(SCRIPTS, "register_agent_log.py"),
  snippets: null,
};

const HELP = `
agent-execution-logging — enforce AI execution logs across any agent environment

Usage:
  agent-execution-logging <command> [options]

Commands:
  bootstrap   Create the default docs/ logging structure in a repo
  register    Register a new agent/model log file
  snippets    Print integration snippets for AGENTS.md / CLAUDE.md / Cursor

Examples:
  npx agent-execution-logging bootstrap --root .
  npx agent-execution-logging register --agent-label "Claude Opus 4.7" --tool-family "Claude Code" --model "Opus 4.7"
  npx agent-execution-logging snippets

Options for bootstrap:
  --root <path>   Repo root (default: current directory)

Options for register:
  --root          Repo root (default: current directory)
  --agent-label   Human-readable agent name (required)
  --agent-id      Explicit slug (auto-generated if omitted)
  --tool-family   e.g. "Claude Code", "Cursor", "Codex"
  --model         e.g. "Opus 4.7", "GPT-5"
  --notes         Optional notes for the registry row
`.trim();

function findPython() {
  for (const bin of ["python3", "python"]) {
    try {
      const v = execFileSync(bin, ["--version"], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
      if (/Python 3/.test(v)) return bin;
    } catch {}
  }
  return null;
}

const [, , cmd, ...rest] = process.argv;

if (!cmd || cmd === "--help" || cmd === "-h") {
  console.log(HELP);
  process.exit(0);
}

if (cmd === "snippets") {
  const fs = require("fs");
  const snippets = path.join(REFS, "integration-snippets.md");
  process.stdout.write(fs.readFileSync(snippets, "utf8"));
  process.exit(0);
}

if (!COMMANDS[cmd]) {
  console.error(`Unknown command: ${cmd}\n`);
  console.log(HELP);
  process.exit(1);
}

const python = findPython();
if (!python) {
  console.error("Python 3 is required but was not found on PATH.");
  process.exit(1);
}

try {
  execFileSync(python, [COMMANDS[cmd], ...rest], { stdio: "inherit" });
} catch (err) {
  process.exit(err.status ?? 1);
}
