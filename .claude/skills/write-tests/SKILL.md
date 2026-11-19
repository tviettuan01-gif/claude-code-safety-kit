---
name: write-tests
description: Write or extend automated tests for a given file, function or behaviour using the project's existing test framework. Use when the user asks for tests, more coverage, or a regression test for a bug.
---

# Write tests

1. Find the test framework and an existing test file near the target (see the Commands table in CLAUDE.md).
2. Read the target code. List the behaviours to cover: normal case, edge cases, error cases.
3. Write tests in the same style as existing tests. Use fixtures or mock data only, never real credentials or production data.
4. Run only the new test file. Fix the test (not the code) if the test is wrong; if the code is wrong, report it and ask before changing it.
5. Summarise: tests added, what they cover, how to run them.
