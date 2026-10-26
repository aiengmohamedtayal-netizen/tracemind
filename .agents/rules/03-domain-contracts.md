---
trigger: always_on
---

# Domain Models and Shared Contracts

`app/domain/models.py` and `app/domain/contracts.py` are the shared contract boundary. Follow the currently agreed ownership rules in `docs/TEAM_WORKFLOW.md`.

- Reuse the canonical `SecurityEvent`, `Evidence`, `EvidenceRelation`, `Hypothesis`, `InvestigationState`, `CandidateAction`, `AgentDecision`, `ActionResult`, `TimelineEntry`, and `Investigation` definitions where they exist.
- Do not define duplicate enums, dataclasses, DTOs, or Protocols in feature modules.
- Use type hints on public functions and explicit result DTOs for stable module boundaries.
- Avoid `Any` and unstructured `dict` in public contracts unless the data is inherently open-ended, such as preserved raw log fields; explain such uses.
- Validate ranges and invariants at appropriate boundaries: scores should be finite and in their documented ranges, timestamps should be timezone-aware and normalized consistently, and IDs should be stable.
- Document optional versus required fields.
- Do not mutate public model semantics without checking all consumers and tests.
- For changes to shared models/contracts: list consumers, propose the exact contract diff, update mock fixtures, and add regression tests.
- When persistence stores a decision and candidate actions, preserve the relation between a decision and its options and ensure the selected action belongs to that decision.
- Treat database constraints as guarantees only if they are present and tested in actual DDL.
