---
trigger: always_on
---

# Documentation and Diagram Synchronization

- Treat `docs/ARCHITECTURE.md` as the main entry point unless repository governance explicitly changes it.
- Consult the supporting design documents for module-specific changes.
- If code behavior, a public contract, database schema, ownership boundary, or workflow changes, update all affected documents in the same work item.
- Mermaid diagrams and rendered assets must describe the same architecture as the text and implementation.
- Inspect `diagram/render_all_diagrams.py` before using it; confirm its output paths stay within the repository.
- Do not generate files outside the repository.
- Do not claim all links or diagrams are valid unless they have actually been checked.
- Avoid maintaining duplicate architecture specs with conflicting content; flag duplicates for owner review rather than deleting them without approval.
