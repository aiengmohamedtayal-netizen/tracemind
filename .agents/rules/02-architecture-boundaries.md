---
trigger: always_on
---

# Architecture and Dependency Rules

TraceMind uses a modular monolith with explicit boundaries.

## Layers
- `app/domain/`: shared domain entities, enums, value objects, typed DTOs, and Protocol contracts.
- `app/application/`: use cases, workflow orchestration, and simulated-action dispatch.
- `app/ingestion/`: parsing, validation, normalization, and deduplication.
- `app/correlation/`: correlation rules and NetworkX evidence graph construction.
- `app/agent/`: perception over the current state, candidate generation, utility evaluation, action selection, and decision explanation.
- `app/investigation/`: hypothesis evaluation and timeline construction.
- `app/infrastructure/`: SQLite connection management, repositories, and configuration.
- `app/ui/`: Streamlit presentation only.
- `app/reporting/`: report assembly and export.
- `tests/`: unit, integration, and end-to-end tests.

## Dependency constraints
- Domain types must not import Streamlit, SQLite implementation details, filesystem UI code, or concrete infrastructure services.
- The Agent Core must not execute actions, read files, access SQLite, or import Streamlit. It returns a typed decision.
- The application/orchestration layer dispatches actions through an explicit simulation execution contract.
- New raw log payloads returned by the simulator must pass through ingestion and validation before being treated as events or evidence.
- The UI calls application services and renders typed results. It must not contain business rules, utility scoring, direct SQL, or repository implementation logic.
- Repositories implement persistence boundaries; domain logic must not depend on a concrete SQLite connection.
- Avoid circular imports and hidden cross-module calls.
- Do not create duplicate models, parsers, utilities, or alternate service layers.

## Architecture changes
- Do not silently change public contracts, data models, status enums, or persisted schema.
- For a cross-cutting change, identify affected modules, docs, tests, and migration impact first.
- Update architecture docs and tests together with an approved implementation change.
