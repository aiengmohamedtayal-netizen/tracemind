---
trigger: always_on
---

# TraceMind — Project Mandate

## Mission
TraceMind is a local, academic Intelligent Cyber Incident Investigator. It ingests authorized or synthetic security logs, correlates evidence, maintains competing hypotheses, chooses simulated investigation actions using utility-based reasoning, records feedback, and explains its decisions.

## Source of truth
Before making a change, consult the relevant repository documents:
- `docs/ARCHITECTURE.md` — master architecture
- `docs/DOMAIN_MODEL.md` — canonical entities and contracts
- `docs/DATA_MODEL.md` — SQLite schema and persistence rules
- `docs/AGENT_DESIGN.md` — agent behavior and utility model
- `docs/CORRELATION_ENGINE.md` — correlation rules and graph semantics
- `docs/TEAM_WORKFLOW.md` — ownership and collaboration
- `docs/IMPLEMENTATION_PLAN.md` — roadmap and MVP boundaries
- `docs/TEST_STRATEGY.md` — verification requirements

If documents conflict, do not silently choose one. Identify the discrepancy, prefer the explicitly designated master document only provisionally, and report the conflict before making a cross-cutting change.

## Product boundaries
- Keep the solution a Python modular monolith unless an approved architecture decision changes that.
- Keep operations local and deterministic where practical.
- Use synthetic data or data explicitly authorized for this project.
- Treat this as an investigation simulator, not a production SOC platform.
- Do not add cloud dependencies, LLM APIs, services, frameworks, or infrastructure without a demonstrated requirement and approval.

## Working discipline
- Inspect existing code, tests, Git status, and relevant docs before changing anything.
- Make the smallest coherent change that satisfies the task.
- Do not claim a feature, test, diagram, or security check passed unless you actually verified it.
- Clearly distinguish implemented behavior, planned design, assumptions, and known limitations.
