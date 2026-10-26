---
trigger: always_on
---

# Streamlit UI and Reporting Rules

- Use Streamlit for presentation and interaction; use Plotly for visualizations as described in the architecture.
- Pages call typed application services; do not put domain/agent logic or direct SQL in UI pages.
- Keep session-state usage small, explicit, and documented.
- Treat Streamlit reruns as normal; design reads to be safe to repeat and avoid accidentally re-running state-changing actions on every rerun.
- Require explicit user interaction to start or advance an investigation.
- Clearly distinguish observed events, derived evidence, hypotheses, simulated actions, and final findings in labels and visualizations.
- Show heuristic confidence as a score, not a verified probability.
- Include provenance and decision explanations where relevant.
- Handle empty states, parse errors, missing data, long labels, and graph density gracefully.
- Keep charts accessible: clear titles, labels, legends, and non-color-only status indications.
- Do not display secrets or unnecessary raw sensitive data in the UI or reports.
