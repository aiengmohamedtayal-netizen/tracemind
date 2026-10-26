# TraceMind — Repository Guide

> **Intelligent Cyber Incident Investigator** — a local, simulation-first academic project that investigates synthetic or explicitly authorized security logs using evidence correlation, competing hypotheses, and utility-based agent decisions.

**Repository:** [aiengmohamedtayal-netizen/tracemind](https://github.com/aiengmohamedtayal-netizen/tracemind)

## Start here

New to the project? Follow this order:

1. **Understand the idea:** read this README.
2. **Understand the system:** read [Architecture](docs/ARCHITECTURE.md).
3. **Understand shared types:** read [Domain Model](docs/DOMAIN_MODEL.md).
4. **Understand storage:** read [Data Model](docs/DATA_MODEL.md).
5. **Understand the agent:** read [Agent Design](docs/AGENT_DESIGN.md).
6. **Understand your team role:** read [Team Workflow](docs/TEAM_WORKFLOW.md) and [Implementation Plan](docs/IMPLEMENTATION_PLAN.md).
7. **Before coding:** read [Test Strategy](docs/TEST_STRATEGY.md).

## What does TraceMind do?

TraceMind demonstrates a stateful intelligent-agent investigation cycle:

```text
Synthetic CSV/JSON logs
        ↓
Ingestion and normalization
        ↓
Evidence correlation graph
        ↓
Hypotheses + missing evidence
        ↓
Agent evaluates candidate actions with U(a) = B(a) - C(a) - R(a)
        ↓
An action is selected and executed in a local simulation
        ↓
New simulated log payloads return through ingestion
        ↓
State, hypotheses, timeline, and explanation are updated
```

**Safety boundary:** TraceMind is an investigation simulator. It must not run offensive operations, access unauthorized systems, or perform automated remediation on real infrastructure. Confidence values are heuristic scores unless formally validated; correlation is not causation.

## Repository map

| Path | Purpose |
|---|---|
| `app/domain/` | Canonical domain models, enums, DTOs, and shared contracts |
| `app/ingestion/` | CSV/JSON parsing, validation, normalization, and deduplication |
| `app/correlation/` | Evidence correlation rules and NetworkX graph construction |
| `app/agent/` | Candidate generation, utility scoring, action selection, and explanations |
| `app/investigation/` | Hypothesis lifecycle and investigation timeline |
| `app/application/` | Use cases, orchestration, and simulated action execution |
| `app/infrastructure/` | SQLite connection, schema, repositories, and configuration |
| `app/ui/` | Streamlit pages and visualizations; presentation only |
| `app/reporting/` | Investigation report assembly and export |
| `data/raw/` | Sample synthetic security logs |
| `data/scenarios/` | Repeatable investigation scenarios |
| `tests/` | Unit, integration, and end-to-end tests |
| `docs/` | Architecture, domain/data models, agent design, team workflow, plan, and tests |
| `.agents/rules/` | Repository-specific instructions for supported AI coding agents, if installed |

> The repository may still contain placeholder modules. A documented component is not necessarily implemented or tested yet. Check the code and test results before assuming it is complete.

## Architecture documentation

- [System architecture](docs/ARCHITECTURE.md)
- [Domain model and service contracts](docs/DOMAIN_MODEL.md)
- [SQLite data model](docs/DATA_MODEL.md)
- [Intelligent-agent design](docs/AGENT_DESIGN.md)
- [Evidence correlation engine](docs/CORRELATION_ENGINE.md)
- [Team workflow and code ownership](docs/TEAM_WORKFLOW.md)
- [Four-week implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Test strategy](docs/TEST_STRATEGY.md)
- [Architecture decision records](docs/ADR/)

Architecture diagrams are in [docs/diagrams/](docs/diagrams/). Start with the system-context diagram, component architecture, agent decision loop, and database ERD.

## Team of six — ownership overview

Use the detailed and current ownership matrix in [docs/TEAM_WORKFLOW.md](docs/TEAM_WORKFLOW.md). The high-level workstreams are:

| Member | Main workstream |
|---|---|
| M1 | Ingestion and SQLite persistence |
| M2 | Evidence correlation and graph |
| M3 | Pure intelligent-agent core and utility scoring |
| M4 | Hypotheses and timeline |
| M5 | Streamlit UI and reporting |
| M6 | Shared contracts, application orchestration, integration and E2E |

Every member owns unit tests for their own module. M6 coordinates cross-module integration and end-to-end verification; shared contracts must not be changed unilaterally.

## Setup

Use Python 3.11+ unless the project configuration documents a different supported version.

### 1. Clone the repository

```bash
git clone https://github.com/aiengmohamedtayal-netizen/tracemind.git
cd tracemind
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Inspect the current test baseline

```bash
python -m pytest
```

If tests or application commands are not yet implemented, record that as the current baseline rather than claiming the system works end-to-end.

## How to contribute

1. Read the relevant architecture docs and identify the module owner.
2. Check `git status` before editing; do not overwrite uncommitted work.
3. Create a focused branch, e.g. `feature/M2-correlation-rules`.
4. Implement only the agreed scope and add tests.
5. Run relevant tests and inspect `git diff`.
6. Open a pull request that explains the change, tests, risks, and documentation updates.
7. For shared model/contract changes, coordinate with M6 and all affected consumers first.

Avoid force pushes, destructive Git commands, unrelated refactors, and committing secrets, `.env` files, virtual environments, caches, or local database files.

## Definition of done

A change is ready for review when:
- It follows documented module boundaries and shared contracts.
- Expected and failure paths have meaningful tests.
- Relevant tests have actually been run and their outcomes are reported honestly.
- Security, provenance, and error handling are considered.
- Architecture or setup docs are updated when behavior or interfaces change.
- The diff contains only changes relevant to the task.

## Project status

This repository includes architecture specifications, sample data, initial shared models/infrastructure, and project scaffolding. Do not assume every module in the roadmap is already implemented. Use the [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) and verified tests to distinguish planned work from completed functionality.
