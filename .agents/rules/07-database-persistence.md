---
trigger: always_on
---

# SQLite and Persistence Rules

- Follow `docs/DATA_MODEL.md`, but verify the actual implementation under `app/infrastructure/` before changing persistence.
- Never assume documentation and current DDL are identical; compare them.
- Enable SQLite foreign-key enforcement on every connection and test it.
- Use parameterized SQL; never interpolate untrusted values into SQL.
- Keep schema initialization/migrations explicit and repeatable.
- Use transactions for multi-entity writes; roll back atomically on failure.
- Do not use `INSERT OR REPLACE` without checking its delete-and-reinsert semantics and foreign-key effects. Prefer an explicit UPSERT where appropriate.
- Add indexes based on documented query patterns, not speculation.
- Keep a repository boundary between business logic and database code.
- Test foreign keys, unique/partial indexes, CHECK constraints, rollback, reloading, duplicate writes, and deletion behavior.
- Ensure selected candidate actions reference options belonging to the same decision, and do not claim a relational invariant is enforced unless the schema enforces it.
- Do not commit SQLite runtime database files unless explicitly requested as an intentional fixture.
