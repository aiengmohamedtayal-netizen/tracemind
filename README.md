# TraceMind — Intelligent Cyber Incident Investigator

> **Autonomous Investigation & Incident Response System** designed for the Intelligent Agents course.  
> Transform cybersecurity telemetry into correlated evidence graphs, evolving hypotheses, and optimal investigation actions using goal-driven utility theory.

---

## 🔍 System Overview

TraceMind is a specialized intelligent agent designed to automate and assist in digital forensics and incident response (DFIR). The agent continuously perceives security events, normalizes and correlates artifacts into an evidence graph, maintains and tracks competing hypotheses, and executes high-utility simulated actions to resolve uncertainty.

```
Perception ──► Ingestion & Normalization ──► Evidence Correlation Graph
                                                       │
                                                       ▼
Feedback ◄── Simulated Action ◄── Utility Reasoning ◄── Hypotheses & Timeline
```

---

## 📁 Repository Structure

```
tracemind/
├── app/
│   ├── agent/                 # Intelligent Agent reasoning, utility calculator & decision loop
│   ├── application/           # Application service orchestration & use cases
│   ├── correlation/           # Evidence correlation engine, rules & NetworkX graph builder
│   ├── domain/                # Canonical domain models (models.py) & contracts (contracts.py)
│   ├── infrastructure/        # SQLite database manager (database.py) & configuration (config.py)
│   ├── ingestion/             # CSV/JSON parsers, normalizer & deduplication
│   ├── investigation/         # Hypothesis engine & timeline builder
│   ├── reporting/             # Incident report generation & executive summary export
│   └── ui/                    # Streamlit dashboard pages & interactive visualizations
├── data/
│   ├── raw/                   # Raw simulated log files (CSV, JSON)
│   ├── normalized/            # Cleaned, normalized security events
│   └── scenarios/             # Pre-configured test scenarios (Brute Force, Lateral Movement, etc.)
├── docs/                      # Architectural specifications & design documents
│   ├── ARCHITECTURE.md        # Master System Architecture & Engineering Plan
│   ├── DOMAIN_MODEL.md        # Canonical Domain Models & Class Diagrams
│   ├── DATA_MODEL.md          # SQLite Schema, DDL & Relational Constraints
│   ├── AGENT_DESIGN.md        # PEAS Agent Specification & Utility Function
│   ├── CORRELATION_ENGINE.md  # Multi-heuristic Evidence Graph Engine
│   ├── TEAM_WORKFLOW.md       # 6-Developer Ownership & Integration Plan
│   ├── IMPLEMENTATION_PLAN.md # 4-Week Milestone Roadmap
│   ├── TEST_STRATEGY.md       # Verification & Scenario Test Matrix
│   ├── ADR/                   # Architecture Decision Records
│   └── diagrams/              # High-resolution architectural diagram assets (PNG)
├── diagram/                   # Diagram rendering assets and scripts
├── scripts/                   # Utility and data generation scripts
└── tests/                     # Unit, integration, and E2E scenario test suites
```

---

## 📚 Architectural Documentation

All core design specifications are available in the [`docs/`](./docs) directory:

- 📐 [**System Architecture (ARCHITECTURE.md)**](./docs/ARCHITECTURE.md) — Comprehensive architecture, context, component diagrams, and modular monolith design.
- 📦 [**Domain Model (DOMAIN_MODEL.md)**](./docs/DOMAIN_MODEL.md) — Data contracts, entity definitions, and lifecycle states.
- 🗄️ [**Data Model (DATA_MODEL.md)**](./docs/DATA_MODEL.md) — SQLite schema, ERD diagrams, and referential integrity constraints.
- 🧠 [**Agent Design (AGENT_DESIGN.md)**](./docs/AGENT_DESIGN.md) — PEAS framework, utility calculation $U(a) = B(a) - C(a) - R(a)$, and action space.
- 🕸️ [**Correlation Engine (CORRELATION_ENGINE.md)**](./docs/CORRELATION_ENGINE.md) — Multi-heuristic correlation rules and NetworkX graph construction.
- 👥 [**Team Workflow & Ownership (TEAM_WORKFLOW.md)**](./docs/TEAM_WORKFLOW.md) — 6-developer team matrix, PR policies, and interface contracts.
- 🗓️ [**Implementation Plan (IMPLEMENTATION_PLAN.md)**](./docs/IMPLEMENTATION_PLAN.md) — 4-week roadmap and milestone gates.
- 🧪 [**Test Strategy (TEST_STRATEGY.md)**](./docs/TEST_STRATEGY.md) — Test pyramid, synthetic scenarios, and acceptance criteria.

---

## 🖼️ Architectural Diagrams

High-resolution visual diagrams are located in [`docs/diagrams/`](./docs/diagrams/):
- **01: System Context** (`01_System_Context_Diagram.png`)
- **02: Component Architecture** (`02_Component_Architecture.png`)
- **03: Data Flow Sequence** (`03_Data_Flow_Sequence.png`)
- **04: Domain Model Class Diagram** (`04_Domain_Model_Class_Diagram.png`)
- **05: Hypothesis State Lifecycle** (`05_Hypothesis_State_Lifecycle.png`)
- **06: SQLite Database ERD** (`06_SQLite_ERD_Diagram.png`)
- **07: Agent Decision Loop** (`07_Agent_Decision_Loop.png`)
- **08: Evidence Correlation Graph** (`08_Evidence_Correlation_Graph.png`)
- **09: Team Dependency Graph** (`09_Team_Dependency_Graph.png`)
- **10: Testing Pyramid** (`10_Testing_Pyramid.png`)
- **11: Four-Week Implementation Roadmap** (`11_Four_Week_Roadmap.png`)
- **12: First Vertical Slice** (`12_First_Vertical_Slice.png`)

---

## ⚖️ License & Attribution

Designed and developed for university academic study in **Intelligent Agents** and **Autonomous Cyber Defense**.
