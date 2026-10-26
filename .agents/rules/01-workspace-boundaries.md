---
trigger: always_on
---

# Workspace Boundaries and File Safety

- Work only inside the opened TraceMind repository.
- Use repository-relative paths whenever possible.
- Do not read, create, edit, move, rename, or delete files outside this repository unless the user explicitly requests it.
- Do not inspect unrelated repositories, personal documents, browser profiles, SSH keys, credential stores, or system configuration.
- Never use broad destructive filesystem operations.
- Never overwrite an existing file before reading it and understanding the diff.
- Before changing generated diagrams, inspect the generator and its intended outputs.
- Do not write generated artifacts to Desktop, Documents, Downloads, Temp, or home directories.
- If a requested task requires access outside the repository, explain why and ask for explicit permission first.
- Preserve user changes. If the working tree is dirty, inspect the affected diff and avoid overwriting those changes.
- Treat symbolic links and paths resolving outside the repository as out of scope unless explicitly approved.
