---
trigger: always_on
---

# Required Protocol for Agent-Assisted Tasks

For non-trivial tasks:

1. **Inspect**: read relevant docs, current code, tests, and Git status.
2. **Scope**: identify the exact outcome and out-of-scope work.
3. **Plan**: list affected modules/files and main risks.
4. **Implement**: make focused changes within agreed ownership and architecture.
5. **Test**: run relevant checks; do not claim unrun checks passed.
6. **Review**: inspect diffs, public contract effects, security, error handling, and documentation consistency.
7. **Report**: summarize changes, files touched, commands/tests and results, limitations, and remaining work.

Additional safeguards:
- If user asks for design/review only, do not edit files.
- If user asks for documentation only, write only within approved documentation paths.
- If user asks for implementation, do not refactor unrelated areas.
- If destructive action, external write, schema migration, or history rewrite is required, stop and request explicit approval.
- Never continue implementation merely because a design task mentioned code examples or repository structure.
