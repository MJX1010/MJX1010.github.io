---
name: "privacy-scan"
description: "Scans staged or target files for personal information and secrets. Invoke before commit/push, when auditing privacy leaks, or when the user asks to prevent sensitive uploads."
---

# Privacy Scan

Use this skill when the task is about preventing personal information, secrets, or credentials from entering Git history, or when the user asks to audit a change set for privacy leaks.

## When To Invoke

- Invoke before running `git add`, `git commit`, or `git push`.
- Invoke when the user asks to scan for emails, phone numbers, ID numbers, API keys, tokens, or private keys.
- Invoke when a document or script batch may contain copied account details or configuration secrets.
- Do not invoke for ordinary content edits that are guaranteed to stay local and never enter version control.

## Goals

- Detect obvious personal information before commit.
- Detect high-risk credential patterns before upload.
- Force a redact-or-move decision instead of allowing "upload first, fix later".
- Keep temporary scan worktrees and analysis output out of the commit scope.

## Workflow

1. Read `.trae/skills/index.md` and `Agent.md` first.
2. Run `python scripts/harness.py privacy-scan --path <scope>`.
3. Review all reported findings and classify them as:
   - real private data that must be removed
   - real secrets that must be rotated and removed
   - safe placeholders that should be rewritten more clearly
4. Move private material to `private/` when it must remain in the knowledge base.
5. Replace examples with `your_email@example.com`, `placeholder`, `dummy`, or other clearly fake values.
6. Re-run the scan until the result is clean.
7. Only then continue with `python scripts/harness.py sync-git ...`.

## Commands

```bash
python scripts/harness.py privacy-scan --path scripts --path .trae --path Agent.md
```

```bash
python scripts/harness.py sync-git --message "update docs" --path scripts --path .trae --path Agent.md
```

## Output Format

- Scan scope
- Finding count
- Sensitive pattern types
- Files that must be redacted or moved
- Confirmation that the re-run result is clean
