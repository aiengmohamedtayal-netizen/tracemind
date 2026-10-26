---
trigger: always_on
---

# Dependencies and Configuration

- Keep dependencies minimal and justified by the project proposal.
- Before adding a package, check whether the standard library or an existing dependency is sufficient.
- Update `requirements.txt` and explain why a new dependency is necessary.
- Pin or constrain versions when appropriate for reproducibility, but do not invent compatibility claims without testing.
- Keep configurable thresholds, correlation windows, and utility weights centralized in the existing configuration module.
- Avoid duplicated hard-coded constants across components.
- Fail clearly when configuration is invalid; do not silently fall back to values that change investigation behavior.
- Do not add external network calls, telemetry, cloud services, or LLM APIs without explicit approval.
