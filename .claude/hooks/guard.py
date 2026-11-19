#!/usr/bin/env python3
"""PreToolUse guard for Claude Code.

Blocks (exit code 2, reason on stderr):
  - destructive shell commands (rm -rf /, force push, DROP TABLE, disk wipes...)
  - reading or editing secret files (.env, private keys, credentials)

Edit BLOCKED_COMMANDS / SECRET_PATTERNS to fit your project.
Stdlib only. Works on Windows, macOS and Linux.
"""
import json
import re
import sys

BLOCKED_COMMANDS = [
    (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b", "recursive force delete (rm -rf)"),
    (r"\bRemove-Item\b.*-Recurse\b.*-Force\b|\bRemove-Item\b.*-Force\b.*-Recurse\b", "recursive force delete (Remove-Item)"),
    (r"\bgit\s+push\b.*(--force\b|-f\b|--force-with-lease\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    (r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b", "dropping database objects"),
    (r"\bmkfs(\.\w+)?\b|\bdd\s+if=.*\bof=/dev/", "disk format / overwrite"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777"),
    (r"curl\b[^|]*\|\s*(sh|bash|python)\b|wget\b[^|]*\|\s*(sh|bash)\b", "piping a download into a shell"),
]

SECRET_PATTERNS = [
    r"(^|[\\/])\.env(\.[\w.-]+)?$",
    r"(^|[\\/])\.env(\.[\w.-]+)?(\s|$|['\"])",
    r"\.(pem|key|p12|pfx)$",
    r"(^|[\\/])id_(rsa|ed25519|ecdsa)(\.pub)?$",
    r"(^|[\\/])(credentials|secrets?)(\.\w+)?$",
    r"(^|[\\/])\.aws[\\/]credentials$",
]
ALLOWED_SECRET_EXAMPLES = re.compile(r"\.env\.(example|sample|template)([\w.-]*)$", re.IGNORECASE)


def is_secret_path(path: str) -> bool:
    if not path or ALLOWED_SECRET_EXAMPLES.search(path):
        return False
    return any(re.search(p, path, re.IGNORECASE) for p in SECRET_PATTERNS)


def block(reason: str) -> None:
    print(f"Blocked by project safety hook: {reason}. Ask the user to do this manually if it is really needed.", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never break Claude Code on malformed input

    tool = data.get("tool_name", "")
    tin = data.get("tool_input", {}) or {}

    if tool in ("Bash", "PowerShell"):
        cmd = tin.get("command", "")
        for pattern, label in BLOCKED_COMMANDS:
            if re.search(pattern, cmd, re.IGNORECASE):
                block(label)
        for token in re.split(r"[\s;|&<>]+", cmd):
            token = token.strip("'\"")
            if is_secret_path(token):
                block(f"command touches a secret file ({token})")

    if tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
        path = tin.get("file_path", "") or tin.get("notebook_path", "")
        if is_secret_path(path):
            block(f"secret file ({path})")

    sys.exit(0)


if __name__ == "__main__":
    main()
