---
trigger: always_on
---

# Hypothesis and Timeline Rules

## Hypotheses
- Preserve separate supporting and contradicting evidence associations.
- Track missing evidence explicitly; absence of data is not automatically contradictory evidence.
- Treat scores as heuristic confidence indicators unless a validated probabilistic model is implemented.
- Keep thresholds and scoring coefficients configurable.
- Do not mark a hypothesis `CONFIRMED` solely because a numeric threshold was crossed.
- Define allowed status transitions and test invalid transitions.
- Human escalation is distinct from confirmation.
- Record why each confidence/status update occurred and which evidence changed it.
- Avoid double-counting the same evidence through multiple derived relationships.

## Timeline
- Build a consistent chronological record for observed events, evidence discoveries, decisions, simulated action results, and hypothesis changes.
- Preserve event time separately from processing/decision time when both matter.
- Normalize timezone handling and define how missing timestamps are represented.
- Use stable sorting tie-breaks for equal timestamps.
- Keep timeline generation out of Streamlit.
- Do not imply causality from chronological order alone.
