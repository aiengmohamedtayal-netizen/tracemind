---
trigger: always_on
---

# Six-Member Collaboration Rules

Follow the current ownership matrix in `docs/TEAM_WORKFLOW.md`; it overrides informal assumptions.

Expected workstreams:
- M1: ingestion and persistence as currently assigned.
- M2: evidence correlation and graph.
- M3: pure intelligent-agent core.
- M4: hypothesis and timeline.
- M5: Streamlit UI and reporting.
- M6: shared contracts, orchestration, integration and E2E quality.

## Collaboration
- Each owner writes unit tests for their own module.
- M6 owns cross-module integration and end-to-end tests, not every unit test.
- Use agreed models, Protocols, and test fixtures to enable parallel development.
- Do not let two members independently modify the same module or shared contract without coordination.
- Open a change request before a shared model/contract/schema change; list affected consumers and update docs, tests, and mocks.
- Use feature branches and small PRs according to `docs/TEAM_WORKFLOW.md`.
- Never push directly to protected/shared branches if the team workflow requires PR review.
- PRs must explain intent, affected architecture, tests run, risks, and any documentation updates.
- Resolve conflicts by discussing the contract/ownership first; do not silently choose one version.
