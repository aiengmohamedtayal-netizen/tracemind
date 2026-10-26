---
trigger: always_on
---

# Testing and Quality Gates

Consult `docs/TEST_STRATEGY.md` for the agreed scenario matrix.

## Every change
- Add or update tests for behavior changes and bug fixes.
- Run the smallest relevant unit-test set first, then integration/E2E tests when feasible.
- Report exact commands and outcomes; distinguish not-run tests from passing tests.
- Do not weaken assertions or delete tests simply to obtain a green run.
- Use deterministic synthetic fixtures and fixed timestamps where practical.

## Important coverage
- Ingestion: CSV/JSON, malformed rows, absent fields, timestamps, duplicates, encoding and invalid values.
- Correlation: each rule in both matching and non-matching cases, threshold boundaries, parallel edge types, isolated events, missing attributes.
- Agent: candidate generation, utility arithmetic, score validation, ties, stopping conditions, failed actions, explanation traceability, deterministic replay.
- Hypotheses: supportive/contradictory/missing evidence, transitions, score boundaries, no premature confirmation.
- Persistence: foreign keys, constraints, transaction rollback, round trips, and relationship consistency.
- UI/orchestration: explicit action triggering, correct handling of service failures, and complete simulated feedback cycle.

## Quality
- Prefer readable code over clever code.
- Tests must assert meaningful behavior, not implementation trivia.
- Do not promise a coverage percentage unless it is measured.
