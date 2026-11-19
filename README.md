# Claude Code Safety Kit

A small, safe-by-default starter for Claude Code in any repository.

## What's inside
| Path | Purpose |
|---|---|
| `CLAUDE.md.template` | Project guide for Claude: stack, commands, conventions, rules. Rename to `CLAUDE.md` and fill in. |
| `.claude/settings.json` | Permission rules (deny reading `.env`, keys) + registers the safety hook. |
| `.claude/hooks/guard.py` | `PreToolUse` hook. Blocks `rm -rf`, force push, `git reset --hard`, `DROP TABLE`, `curl … \| bash`, and reading/editing secret files. |
| `.claude/skills/release-notes` | `/release-notes`: draft release notes since the last tag. |
| `.claude/skills/review-diff` | `/review-diff`: review the current diff against CLAUDE.md. |
| `.claude/skills/write-tests` | `/write-tests`: add tests with the project's framework. |
| `tests/test_guard.py` | 21 checks for the hook (`python tests/test_guard.py`). |

## Install
1. Copy `.claude/` and `CLAUDE.md.template` into your repo root.
2. Rename `CLAUDE.md.template` to `CLAUDE.md` and replace every `{{...}}`.
3. Requires Python 3.8+ on PATH as `python`. (On macOS/Linux, if you only have `python3`, edit the command in `.claude/settings.json`.)
4. Start Claude Code in the repo and run `/hooks` to confirm the hook is registered.

## Try it
Ask Claude: *"run rm -rf build"* or *"show me the .env file"*. The hook blocks it and tells Claude to ask you instead.

## Customise
- Add patterns to `BLOCKED_COMMANDS` / `SECRET_PATTERNS` in `guard.py`.
- Hooks are a safety net, not a sandbox: keep secrets out of the repo and use test credentials.

License: MIT.
