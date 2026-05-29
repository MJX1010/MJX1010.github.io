---
name: "link-audit"
description: "Audits and fixes Markdown external links. Invoke when the user asks to scan, repair, archive, or batch-clean broken links in notes."
---

# Link Audit

Use this skill when the task is about checking external links in Markdown notes, generating a health report, replacing stale URLs, or archiving dead links as plain text.

## When To Invoke

- Invoke when the user asks to scan `content/` or `private/` for broken links.
- Invoke when the user asks to batch repair `404/403/error` links.
- Invoke when the user asks to convert dead private links into archive text instead of keeping clickable broken links.
- Do not invoke for ordinary text edits unrelated to link governance.

## Goals

- Produce a repeatable link health report.
- Separate public notes from private/login/internal links.
- Replace broken links with more stable official entry points when possible.
- Convert irrecoverable private or stale links into archived plain text.
- Re-run the audit after fixes and report the remaining exceptions.

## Workflow

1. Read `.trae/skills/index.md` and `Agent.md` first for repository rules.
2. Run `python scripts/harness.py audit-links --root content`.
3. Review the generated report under `private/link_audit/`.
4. Classify findings into:
   - replace with stable official entry
   - archive as dead-link text
   - keep as private/restricted reference
5. Write a `scripts/link_fix_plan_*.json` plan file.
6. Apply the plan with `python scripts/harness.py apply-link-plan --plan <plan>`.
7. Re-run the audit and compare the remaining `broken/error/auth` counts.

## References

- Detailed workflow: `references/workflow.md`
- Command examples: `references/commands.md`

## Output Format

- Audit scope
- Report path
- What was replaced
- What was archived
- Remaining exceptions by status
