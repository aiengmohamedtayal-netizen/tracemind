---
trigger: always_on
---

# Git and Release Safety

- Run `git status --short --branch` before editing and before committing.
- Inspect `git diff` and `git diff --cached` before any commit.
- Never run `git reset --hard`, `git clean -fd`, force push, history rewrite, or broad deletion unless the user explicitly requests that exact action and the impact is clear.
- Never discard uncommitted user/team changes.
- Do not stage the entire repository blindly; inspect ignored/untracked files and secrets first.
- Keep `.gitignore` aligned with Python, test, IDE, environment, secret, and local-database artifacts.
- Do not amend or rewrite a commit already shared with others unless the team explicitly agrees.
- Do not push or merge without an explicit task request.
- When asked to publish, verify the exact repository, target branch, local changes, staged diff, and remote history before writing.
- After a push, verify the remote ref and report commit SHA, branch, and test status truthfully.
