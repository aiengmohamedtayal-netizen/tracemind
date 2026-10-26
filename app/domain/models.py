"""
TraceMind — Shared Domain Models
المصدر الوحيد للحقيقة لجميع هياكل البيانات والكيانات المشتركة بين أعضاء الفريق الستة.
Owner: Member 6 (Integration Owner)
Reviewers: All Team Members (Changes require PR & agreement)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


# ============================================================================
# 1. ENUMS (التصنيفات الثابتة)
# ============================================================================

class EventType(str, Enum):
    LOGIN_FAILED = "LOGIN_FAILED"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    NETWORK_CONNECTION = "NETWORK_CONNECTION"
    FILE_ACCESS = "FILE_ACCESS"
    PROCESS_EXEC = "PROCESS_EXEC"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    PORT_SCAN = "PORT_SCAN"
    DATA_EXFILTRATION = "DATA_EXFILTRATION"
    UNKNOWN = "UNKNOWN"


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    DUPLICATE = "DUPLICATE"


class EvidenceType(str, Enum):
    LOG_ENTRY = "LOG_ENTRY"
    NETWORK_ARTIFACT = "NETWORK_ARTIFACT"
    ACCOUNT_ACTIVITY = "ACCOUNT_ACTIVITY"
    DEVICE_ACTIVITY = "DEVICE_ACTIVITY"
    TEMPORAL_PATTERN = "TEMPORAL_PATTERN"
    BEHAVIORAL_INDICATOR = "BEHAVIORAL_INDICATOR"


class RelationType(str, Enum):
    SAME_ACCOUNT = "SAME_ACCOUNT"
    SAME_DEVICE = "SAME_DEVICE"
    TEMPORALLY_RELATED = "TEMPORALLY_RELATED"
    NETWORK_RELATED = "NETWORK_RELATED"
    SAME_INDICATOR = "SAME_INDICATOR"


class HypothesisStatus(str, Enum):
    OPEN = "OPEN"
    SUPPORTED = "SUPPORTED"
    WEAKENED = "WEAKENED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    CONFIRMED = "CONFIRMED"


class ActionType(str, Enum):
    REQUEST_ADDITIONAL_LOGS = "REQUEST_ADDITIONAL_LOGS"
    ANALYZE_RELATED_EVENT = "ANALYZE_RELATED_EVENT"
    INVESTIGATE_ENTITY = "INVESTIGATE_ENTITY"
    REVIEW_EVIDENCE_RELATION = "REVIEW_EVIDENCE_RELATION"
    ESCALATE_FOR_HUMAN_REVIEW = "ESCALATE_FOR_HUMAN_REVIEW"
    CONCLUDE_INVESTIGATION = "CONCLUDE_INVESTIGATION"


class InvestigationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


# ============================================================================
# 2. CORE DOMAIN ENTITIES (الكيانات الأساسية)
# ============================================================================

@dataclass
class SecurityEvent:
    """
    يمثل حدثاً أمنياً بعد الاستيراد والتنظيف والتطبيع.
    """
    id: str
    timestamp: datetime
    event_type: EventType
    severity: Severity
    source_file: str
    validation_status: ValidationStatus = ValidationStatus.VALID
    account_id: Optional[str] = None
    device_id: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    indicator: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    normalized_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type.value,
            "severity": self.severity.value,
            "source_file": self.source_file,
            "validation_status": self.validation_status.value,
            "account_id": self.account_id,
            "device_id": self.device_id,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "indicator": self.indicator,
            "raw_data": self.raw_data,
            "normalized_at": self.normalized_at.isoformat()
        }


@dataclass
class Evidence:
    """
    يمثل دليلاً أمنياً مستخرجاً من حدث أو مجموعة أحداث مع درجة الموثوقية والمصدر.
    """
    id: str
    evidence_type: EvidenceType
    source_event_id: str
    reliability: float  # بين 0.0 و 1.0
    observed_value: str
    timestamp: datetime
    provenance: str
    related_evidence_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "evidence_type": self.evidence_type.value,
            "source_event_id": self.source_event_id,
            "reliability": round(self.reliability, 3),
            "observed_value": self.observed_value,
            "timestamp": self.timestamp.isoformat(),
            "provenance": self.provenance,
            "related_evidence_ids": self.related_evidence_ids
        }


@dataclass
class EvidenceRelation:
    """
    حافة (Edge) في رسم الأدلة (Evidence Graph) توضح العلاقة وقوتها ونوعها.
    Correlation != Causation.
    """
    id: str
    source_evidence_id: str
    target_evidence_id: str
    relation_type: RelationType
    weight: float  # 0.0 - 1.0
    confidence: float  # 0.0 - 1.0
    temporal_delta_seconds: Optional[float] = None
    provenance: str = "correlation_rule"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_evidence_id": self.source_evidence_id,
            "target_evidence_id": self.target_evidence_id,
            "relation_type": self.relation_type.value,
            "weight": round(self.weight, 3),
            "confidence": round(self.confidence, 3),
            "temporal_delta_seconds": self.temporal_delta_seconds,
            "provenance": self.provenance,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Hypothesis:
    """
    فرضية تحقيق أمني تحافظ على مستوى الثقة وسجل التغييرات والأدلة المؤيدة والمعارضة.
    """
    id: str
    description: str
    status: HypothesisStatus = HypothesisStatus.OPEN
    confidence: float = 0.5  # 0.0 - 1.0
    supporting_evidence_ids: List[str] = field(default_factory=list)
    contradicting_evidence_ids: List[str] = field(default_factory=list)
    missing_evidence_types: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    history: List[Dict[str, Any]] = field(default_factory=list)

    def record_transition(self, new_status: HypothesisStatus, new_confidence: float, reason: str):
        self.history.append({
            "previous_status": self.status.value,
            "new_status": new_status.value,
            "previous_confidence": round(self.confidence, 3),
            "new_confidence": round(new_confidence, 3),
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.status = new_status
        self.confidence = max(0.0, min(1.0, new_confidence))
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "confidence": round(self.confidence, 3),
            "supporting_evidence_ids": self.supporting_evidence_ids,
            "contradicting_evidence_ids": self.contradicting_evidence_ids,
            "missing_evidence_types": self.missing_evidence_types,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "history": self.history
        }


@dataclass
class CandidateAction:
    """
    إجراء تحقيق مرشح آمن يتم تقييمه بواسطة دالة المنفعة U(a) = B(a) - C(a) - R(a).
    """
    id: str
    action_type: ActionType
    target_entity: Optional[str]
    description: str
    estimated_benefit: float = 0.0  # B(a)
    estimated_cost: float = 0.0     # C(a)
    estimated_risk: float = 0.0     # R(a)
    utility: float = 0.0            # U(a) = B - C - R
    parameters: Dict[str, Any] = field(default_factory=dict)

    def compute_utility(self) -> float:
        self.utility = round(self.estimated_benefit - self.estimated_cost - self.estimated_risk, 4)
        return self.utility

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "action_type": self.action_type.value,
            "target_entity": self.target_entity,
            "description": self.description,
            "estimated_benefit": round(self.estimated_benefit, 3),
            "estimated_cost": round(self.estimated_cost, 3),
            "estimated_risk": round(self.estimated_risk, 3),
            "utility": round(self.utility, 3),
            "parameters": self.parameters
        }


@dataclass
class AgentDecision:
    """
    سجل قرار الوكيل الذكي موثق بالكامل لضمان القابلية للتفسير والتدقيق (Explainability).
    """
    id: str
    selected_action: CandidateAction
    candidate_actions: List[CandidateAction]
    utility_score: float
    benefit: float
    cost: float
    risk: float
    evidence_ids_used: List[str]
    hypothesis_ids_considered: List[str]
    explanation: str
    investigation_step: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "selected_action": self.selected_action.to_dict(),
            "candidate_actions": [c.to_dict() for c in self.candidate_actions],
            "utility_score": round(self.utility_score, 3),
            "benefit": round(self.benefit, 3),
            "cost": round(self.cost, 3),
            "risk": round(self.risk, 3),
            "evidence_ids_used": self.evidence_ids_used,
            "hypothesis_ids_considered": self.hypothesis_ids_considered,
            "explanation": self.explanation,
            "investigation_step": self.investigation_step,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ActionResult:
    """
    نتيجة تنفيذ الإجراء في البيئة التجريبية / المحاكاة وتغذية راجعة (Feedback).
    """
    id: str
    decision_id: str
    success: bool
    new_evidence_ids: List[str]
    feedback_message: str
    simulated: bool = True
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "decision_id": self.decision_id,
            "success": self.success,
            "new_evidence_ids": self.new_evidence_ids,
            "feedback_message": self.feedback_message,
            "simulated": self.simulated,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class TimelineEntry:
    """
    عنصر في الخط الزمني للتحقيق يربط الأحداث والأدلة وقرارات الوكيل.
    """
    id: str
    timestamp: datetime
    entry_type: str  # "EVENT", "EVIDENCE", "DECISION", "FEEDBACK"
    title: str
    description: str
    event_ids: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    hypothesis_ids: List[str] = field(default_factory=list)
    decision_id: Optional[str] = None
    severity: Optional[Severity] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "entry_type": self.entry_type,
            "title": self.title,
            "description": self.description,
            "event_ids": self.event_ids,
            "evidence_ids": self.evidence_ids,
            "hypothesis_ids": self.hypothesis_ids,
            "decision_id": self.decision_id,
            "severity": self.severity.value if self.severity else None
        }


@dataclass
class InvestigationState:
    """
    الحالة الداخلية الكاملة للوكيل الذكي (Internal Agent State).
    تتحدث ديناميكياً مع كل دورة إدراك وتغذية راجعة.
    """
    investigation_id: str
    current_evidence: List[Evidence] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    timeline: List[TimelineEntry] = field(default_factory=list)
    known_entities: Dict[str, List[str]] = field(default_factory=dict)
    missing_information: List[str] = field(default_factory=list)
    candidate_actions: List[CandidateAction] = field(default_factory=list)
    previous_actions: List[CandidateAction] = field(default_factory=list)
    decision_history: List[AgentDecision] = field(default_factory=list)
    current_step: int = 0
    status: InvestigationStatus = InvestigationStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "investigation_id": self.investigation_id,
            "current_evidence": [e.to_dict() for e in self.current_evidence],
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "timeline": [t.to_dict() for t in self.timeline],
            "known_entities": self.known_entities,
            "missing_information": self.missing_information,
            "candidate_actions": [c.to_dict() for c in self.candidate_actions],
            "previous_actions": [p.to_dict() for p in self.previous_actions],
            "decision_history": [d.to_dict() for d in self.decision_history],
            "current_step": self.current_step,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class Investigation:
    """
    حاوية التحقيق الشاملة المخزنة في النظام.
    """
    id: str
    name: str
    description: str
    source_files: List[str]
    state: InvestigationState
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "source_files": self.source_files,
            "state": self.state.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
