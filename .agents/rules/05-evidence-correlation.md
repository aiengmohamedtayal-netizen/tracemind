---
trigger: always_on
---

# Evidence Correlation and Graph Rules

- Implement correlation rules as focused, deterministic units with named rule IDs.
- Consider shared account, shared device, temporal proximity, network relationships, and shared indicators only as specified by the agreed design.
- Treat correlation as contextual association, never proof of causation or compromise.
- Ignore null/empty identifiers when checking equality; do not create links merely because two records both lack a field.
- Make temporal thresholds and relation weights configurable and documented.
- Define temporal boundary semantics consistently (`<` versus `<=`) and test exact boundary values.
- Preserve provenance: every relationship should identify its rule, source/target, relevant observed fields, temporal delta where applicable, and scoring attributes.
- If multiple distinct relationship types can exist between the same two nodes, use the agreed `MultiDiGraph` representation or another explicitly approved model that preserves each relationship.
- Keep graph construction separate from Plotly rendering.
- Test graph node/edge counts, multiple parallel relations, isolated nodes, duplicates, missing timestamps, invalid fields, and deterministic output.
- Do not combine multiple relation scores in a way that hides their independent meanings.
