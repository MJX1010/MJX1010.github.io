---
name: "note-curation"
description: "Curates imported notes and links into final topic notes. Invoke when the user wants full整理、归档、分流、合并现有笔记，而不是只收集链接。"
---

# Note Curation

Use this skill when the task is to turn imported raw material into final notes under the repository knowledge structure.

## When To Invoke

- Invoke when the user asks to整理 OneTab、收集箱、待分类链接、导入资料或批量补充专题笔记。
- Invoke when the user wants to merge new material into existing topic notes instead of creating a loose link dump.
- Invoke when the user wants public/private split, deduplication, and archive closure for a batch.
- Do not invoke when the task is only to test one URL or tweak one sentence.

## Goals

- Complete each import batch without leaving a lingering “待整理” state.
- Merge information into existing notes first, then create a new topic only if needed.
- Read source content before writing notes; do not paste raw links as the main body.
- Keep public notes reusable and move private/login/internal material out of the public area.

## Workflow

1. Read `Agent.md` and `.trae/skills/index.md`.
2. Enumerate all entries from the import source.
3. Classify them into public, private, or discard.
4. Fetch or inspect source content and extract the usable knowledge.
5. Merge the extracted content into existing notes or a stable new topic note.
6. Run link cleanup and note lint checks when the batch is large.
7. If the batch will be committed, run `python scripts/harness.py privacy-scan --path <scope>` and move any personal or credential-bearing content to `private/`.
8. Convert the import batch into an archived record or remove it entirely.

## References

- Repository rules: `references/rules.md`
- Suggested command flow: `references/commands.md`

## Output Format

- Source batch
- Public notes updated
- Private archive updated
- Discarded items
- Remaining risks or follow-up cleanup
