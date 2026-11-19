---
name: release-notes
description: Draft user-facing release notes from git commits since the last tag. Use when the user asks for release notes, a changelog entry, or "what changed since the last release".
---

# Release notes

1. Find the last tag: `git describe --tags --abbrev=0`. If there is none, ask the user for a starting commit.
2. List commits: `git log <tag>..HEAD --pretty=format:"%h %s"`.
3. Group them under **Added**, **Changed**, **Fixed**, **Removed**. Drop chores, merges and CI-only commits.
4. Rewrite each line for end users: what changed and why it matters, not file names.
5. Show the draft. Do not create tags, commits or files unless the user asks.
