---
trigger: always_on
---

# Intelligent Agent Engineering Rules

The core learning objective is to demonstrate stateful, goal-driven, utility-based agent behavior—not merely fixed alert rules.

## Required lifecycle
Perception → Internal State → Reasoning → Planning/Action Selection → Simulated Execution → Feedback → State Update → Replanning.

## Agent Core
- Keep the Agent Core pure with respect to external effects: it evaluates a supplied state and returns a typed decision.
- Candidate actions must be generated from relevant hypotheses, evidence relationships, unresolved questions, and missing information.
- Evaluate candidate actions using the documented utility function `U(a) = B(a) - C(a) - R(a)`.
- Use named, configurable components for benefit, cost, risk, and weights; avoid unexplained magic numbers.
- Keep score scales consistent and documented; check for NaN, infinity, and invalid score ranges.
- Define deterministic tie-breaking so identical state and configuration produce reproducible decisions.
- Handle empty candidates, failed simulated actions, already-attempted actions, missing payloads, and max-step termination explicitly.
- Avoid repeated selection of the same unproductive action without a state change or justified retry policy.
- Produce explanations that state the selected action, relevant evidence/state, key score components, and remaining uncertainty.
- Store enough decision context to reproduce and audit a decision.
- Do not claim utility or heuristic confidence scores are calibrated probabilities.

## Execution boundary
- The Agent Core selects; the application layer dispatches; the simulator executes; ingestion validates returned payloads; investigation logic updates hypotheses/timeline; the orchestrator updates and persists state.
- Never execute network, endpoint, remediation, or production-changing operations.
- Human escalation is a simulated workflow state, not an automated real-world response.
