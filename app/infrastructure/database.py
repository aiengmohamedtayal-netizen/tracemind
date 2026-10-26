"""
TraceMind — Infrastructure: SQLite Database Manager & Repositories
مسؤولية Member 6 (Integration) بالتعاون مع Member 1.
يوفر دوال تخزين واسترجاع التحقيقات، الأحداث، الأدلة، الفرضيات، وقرارات الوكيل.
"""

from __future__ import annotations
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from app.domain.models import (
    Investigation,
    InvestigationState,
    InvestigationStatus,
    SecurityEvent,
    EventType,
    Severity,
    ValidationStatus,
    Evidence,
    EvidenceType,
    EvidenceRelation,
    RelationType,
    Hypothesis,
    HypothesisStatus,
    CandidateAction,
    ActionType,
    AgentDecision,
    ActionResult,
    TimelineEntry,
)
from app.infrastructure.config import config


class DatabaseManager:
    """إدارة اتصال قاعدة بيانات SQLite وتهيئة المخطط والجداول"""
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or config.db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize_schema(self):
        """إنشاء كافة الجداول والفهارس المطلوبة للنظام"""
        with self.get_connection() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS investigations (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                source_files TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS security_events (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                source_file TEXT NOT NULL,
                validation_status TEXT NOT NULL,
                account_id TEXT,
                device_id TEXT,
                source_ip TEXT,
                destination_ip TEXT,
                indicator TEXT,
                raw_data TEXT,
                normalized_at TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                evidence_type TEXT NOT NULL,
                source_event_id TEXT NOT NULL,
                reliability REAL NOT NULL,
                observed_value TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                provenance TEXT NOT NULL,
                related_evidence_ids TEXT,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS evidence_relations (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                source_evidence_id TEXT NOT NULL,
                target_evidence_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                weight REAL NOT NULL,
                confidence REAL NOT NULL,
                temporal_delta_seconds REAL,
                provenance TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE,
                FOREIGN KEY (source_evidence_id) REFERENCES evidence(id) ON DELETE CASCADE,
                FOREIGN KEY (target_evidence_id) REFERENCES evidence(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS hypotheses (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                confidence REAL NOT NULL,
                supporting_evidence_ids TEXT,
                contradicting_evidence_ids TEXT,
                missing_evidence_types TEXT,
                history TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS candidate_actions (
                id TEXT PRIMARY KEY,
                decision_id TEXT,
                action_type TEXT NOT NULL,
                target_entity TEXT,
                description TEXT NOT NULL,
                estimated_benefit REAL NOT NULL,
                estimated_cost REAL NOT NULL,
                estimated_risk REAL NOT NULL,
                utility REAL NOT NULL,
                parameters TEXT
            );

            CREATE TABLE IF NOT EXISTS agent_decisions (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                investigation_step INTEGER NOT NULL,
                selected_action_id TEXT NOT NULL,
                utility_score REAL NOT NULL,
                benefit REAL NOT NULL,
                cost REAL NOT NULL,
                risk REAL NOT NULL,
                evidence_ids_used TEXT,
                hypothesis_ids_considered TEXT,
                explanation TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS action_results (
                id TEXT PRIMARY KEY,
                decision_id TEXT NOT NULL,
                success INTEGER NOT NULL,
                new_evidence_ids TEXT,
                feedback_message TEXT NOT NULL,
                simulated INTEGER DEFAULT 1,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (decision_id) REFERENCES agent_decisions(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS timeline_entries (
                id TEXT PRIMARY KEY,
                investigation_id TEXT,
                timestamp TEXT NOT NULL,
                entry_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                event_ids TEXT,
                evidence_ids TEXT,
                hypothesis_ids TEXT,
                decision_id TEXT,
                severity TEXT,
                FOREIGN KEY (investigation_id) REFERENCES investigations(id) ON DELETE CASCADE
            );

            -- Indexes for Performance
            CREATE INDEX IF NOT EXISTS idx_events_investigation ON security_events(investigation_id);
            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON security_events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_evidence_investigation ON evidence(investigation_id);
            CREATE INDEX IF NOT EXISTS idx_relations_investigation ON evidence_relations(investigation_id);
            CREATE INDEX IF NOT EXISTS idx_hypotheses_investigation ON hypotheses(investigation_id);
            CREATE INDEX IF NOT EXISTS idx_decisions_investigation ON agent_decisions(investigation_id);
            CREATE INDEX IF NOT EXISTS idx_timeline_investigation ON timeline_entries(investigation_id, timestamp);
            """)

    def save_investigation(self, inv: Investigation) -> str:
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO investigations (id, name, description, status, source_files, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                inv.id,
                inv.name,
                inv.description,
                inv.state.status.value,
                json.dumps(inv.source_files),
                inv.created_at.isoformat(),
                inv.updated_at.isoformat()
            ))

            # حفظ الأدلة
            for e in inv.state.current_evidence:
                conn.execute("""
                    INSERT OR REPLACE INTO evidence (id, investigation_id, evidence_type, source_event_id, reliability, observed_value, timestamp, provenance, related_evidence_ids)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    e.id, inv.id, e.evidence_type.value, e.source_event_id, e.reliability,
                    e.observed_value, e.timestamp.isoformat(), e.provenance, json.dumps(e.related_evidence_ids)
                ))

            # حفظ الفرضيات
            for h in inv.state.hypotheses:
                conn.execute("""
                    INSERT OR REPLACE INTO hypotheses (id, investigation_id, description, status, confidence, supporting_evidence_ids, contradicting_evidence_ids, missing_evidence_types, history, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    h.id, inv.id, h.description, h.status.value, h.confidence,
                    json.dumps(h.supporting_evidence_ids), json.dumps(h.contradicting_evidence_ids),
                    json.dumps(h.missing_evidence_types), json.dumps(h.history),
                    h.created_at.isoformat(), h.updated_at.isoformat()
                ))

            # حفظ القرارات
            for d in inv.state.decision_history:
                conn.execute("""
                    INSERT OR REPLACE INTO agent_decisions (id, investigation_id, investigation_step, selected_action_id, utility_score, benefit, cost, risk, evidence_ids_used, hypothesis_ids_considered, explanation, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    d.id, inv.id, d.investigation_step, d.selected_action.id, d.utility_score,
                    d.benefit, d.cost, d.risk, json.dumps(d.evidence_ids_used),
                    json.dumps(d.hypothesis_ids_considered), d.explanation, d.timestamp.isoformat()
                ))

            # حفظ الخط الزمني
            for t in inv.state.timeline:
                conn.execute("""
                    INSERT OR REPLACE INTO timeline_entries (id, investigation_id, timestamp, entry_type, title, description, event_ids, evidence_ids, hypothesis_ids, decision_id, severity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    t.id, inv.id, t.timestamp.isoformat(), t.entry_type, t.title, t.description,
                    json.dumps(t.event_ids), json.dumps(t.evidence_ids), json.dumps(t.hypothesis_ids),
                    t.decision_id, t.severity.value if t.severity else None
                ))
        return inv.id

    def list_investigations(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT id, name, description, status, created_at, updated_at FROM investigations ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def load_investigation(self, investigation_id: str) -> Optional[Investigation]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM investigations WHERE id = ?", (investigation_id,))
            inv_row = cursor.fetchone()
            if not inv_row:
                return None

            # جلب الأدلة
            cursor = conn.execute("SELECT * FROM evidence WHERE investigation_id = ?", (investigation_id,))
            evidence_list = []
            for r in cursor.fetchall():
                evidence_list.append(Evidence(
                    id=r["id"],
                    evidence_type=EvidenceType(r["evidence_type"]),
                    source_event_id=r["source_event_id"],
                    reliability=r["reliability"],
                    observed_value=r["observed_value"],
                    timestamp=datetime.fromisoformat(r["timestamp"]),
                    provenance=r["provenance"],
                    related_evidence_ids=json.loads(r["related_evidence_ids"] or "[]")
                ))

            # جلب الفرضيات
            cursor = conn.execute("SELECT * FROM hypotheses WHERE investigation_id = ?", (investigation_id,))
            hypotheses = []
            for r in cursor.fetchall():
                hypotheses.append(Hypothesis(
                    id=r["id"],
                    description=r["description"],
                    status=HypothesisStatus(r["status"]),
                    confidence=r["confidence"],
                    supporting_evidence_ids=json.loads(r["supporting_evidence_ids"] or "[]"),
                    contradicting_evidence_ids=json.loads(r["contradicting_evidence_ids"] or "[]"),
                    missing_evidence_types=json.loads(r["missing_evidence_types"] or "[]"),
                    created_at=datetime.fromisoformat(r["created_at"]),
                    updated_at=datetime.fromisoformat(r["updated_at"]),
                    history=json.loads(r["history"] or "[]")
                ))

            # جلب الخط الزمني
            cursor = conn.execute("SELECT * FROM timeline_entries WHERE investigation_id = ? ORDER BY timestamp ASC", (investigation_id,))
            timeline = []
            for r in cursor.fetchall():
                timeline.append(TimelineEntry(
                    id=r["id"],
                    timestamp=datetime.fromisoformat(r["timestamp"]),
                    entry_type=r["entry_type"],
                    title=r["title"],
                    description=r["description"],
                    event_ids=json.loads(r["event_ids"] or "[]"),
                    evidence_ids=json.loads(r["evidence_ids"] or "[]"),
                    hypothesis_ids=json.loads(r["hypothesis_ids"] or "[]"),
                    decision_id=r["decision_id"],
                    severity=Severity(r["severity"]) if r["severity"] else None
                ))

            state = InvestigationState(
                investigation_id=investigation_id,
                current_evidence=evidence_list,
                hypotheses=hypotheses,
                timeline=timeline,
                status=InvestigationStatus(inv_row["status"]),
                created_at=datetime.fromisoformat(inv_row["created_at"]),
                updated_at=datetime.fromisoformat(inv_row["updated_at"])
            )

            return Investigation(
                id=inv_row["id"],
                name=inv_row["name"],
                description=inv_row["description"],
                source_files=json.loads(inv_row["source_files"] or "[]"),
                state=state,
                created_at=datetime.fromisoformat(inv_row["created_at"]),
                updated_at=datetime.fromisoformat(inv_row["updated_at"])
            )
