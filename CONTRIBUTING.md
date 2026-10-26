# Contributing to TraceMind

This guide explains how the six-person team collaborates. Architecture details and module ownership are defined in [docs/TEAM_WORKFLOW.md](docs/TEAM_WORKFLOW.md).

## First contribution

1. Clone the repository and read [README.md](README.md).
2. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
3. Read the domain contract and module-specific design before coding.
4. Check `git status --short --branch` before editing.
5. Confirm module ownership and the expected interface with the owner.

## Branch and PR convention

Use a focused branch such as `feature/M2-correlation-rules` or `fix/M1-csv-validation`. Keep pull requests small and scoped to one change.

Every PR should include:
- **Why:** the problem or requirement addressed.
- **What:** files/modules changed.
- **Contracts:** whether shared models or public interfaces changed.
- **Tests:** exact commands run and truthful results.
- **Risks:** migration, compatibility, security, or follow-up concerns.
- **Docs:** relevant documentation updates.

## Shared contracts

Do not create duplicate domain entities or edit `app/domain/models.py` or `app/domain/contracts.py) unilaterally. Follow the RFC/change process in [docs/TEAM_WORKFLOW.md](docs/TEAM_WORKFLOW.md), coordinate with M6 and affected module owners, and update mocks/tests with the contract change.

## Quality requirements

- Add tests for new behavior and bug fixes.
- Preserve deterministic behavior where practical.
- Keep UI free of business rules and direct SQL.
- Keep the Agent Core free of external side effects.
- Never infer causation from correlation alone.
- Use synthetic or explicitly authorized data.
- Do not commit secrets, environment files, local databases, caches, or virtual environments.

## Git safety

Never force-push, rewrite shared history, or use destructive commands to discard work without explicit team approval. Inspect the diff before committing.
