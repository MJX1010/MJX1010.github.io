---
name: "git-sync-push"
description: "Stages, commits, and pushes workspace changes to Git. Invoke when the user wants one-click sync/upload after local edits and checks are complete."
---

# Git Sync Push

Use this skill when the user wants to update the repository and upload the current changes to Git with a single guided workflow.

## When To Invoke

- Invoke when the user explicitly asks to sync, upload, push, submit, or publish the current workspace changes to Git.
- Invoke after local edits are complete and basic checks have passed.
- Do not invoke for ordinary file edits that are not ready to be committed.

## Goals

- Check the current branch and working tree status.
- Stage the intended changes.
- Create a concise commit message based on the actual diff.
- Push to the current remote branch without force-pushing.
- Report what was committed and what was pushed.

## Workflow

1. Run `git status --short --branch` and inspect the current branch state.
2. Review the diff summary with `git diff --stat` and `git diff --cached --stat` when needed.
3. If there are unexpected changes unrelated to the current task, stop and ask the user how to proceed.
4. Stage the intended files with `git add -A` unless the user requested a narrower commit.
5. Create a commit message that summarizes the actual change set.
6. Run `git commit -m "<message>"`.
7. Push with `git push`.
8. Return the branch, commit hash, and pushed scope.

## Safety Rules

- Never use `git push --force` unless the user explicitly asks for it.
- Never amend an existing commit unless the user explicitly asks for it.
- If push fails because no upstream is set, use `git push -u origin <branch>` only after confirming the remote and branch are correct.
- If the repo has no remote or authentication is missing, stop and report the exact blocker.

## Output Format

- Branch name
- Commit hash
- Commit message
- Push result
- Any follow-up action the user still needs to perform
