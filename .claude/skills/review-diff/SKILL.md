---
name: review-diff
description: Review the current uncommitted diff (or a branch diff) against the project's CLAUDE.md rules. Use when the user asks to review changes, check work before committing, or find bugs in the diff.
---

# Review the diff

1. Get the diff: `git diff` (and `git diff --staged`). If the user names a branch, use `git diff <base>...HEAD`.
2. Read `CLAUDE.md` for the project's conventions and rules.
3. Check, in this order:
   - Correctness: logic errors, unhandled errors, off-by-one, null/undefined.
   - Security: secrets in code, injection, unsafe input handling.
   - Tests: is every behaviour change covered?
   - Conventions from CLAUDE.md.
4. Report findings as a list: `file:line - problem - suggested fix`, most severe first. Say "no issues found" if so.
5. Do not edit files unless the user asks you to apply fixes.
