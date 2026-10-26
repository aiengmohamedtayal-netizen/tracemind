"""
TraceMind — Interface Contracts (Protocols)
عقود الواجهات البرمجية بين الوحدات السبع في المشروع باستخدام Python Protocols.
تتيح هذه العقود لكل عضو تطوير واختبار وحدته باستخدام Stubs و Mocks دون انتظار اكتمال الوحدات الأخرى.
Owner: Member 6 (Integration Owner)
"""

from __future__ import annotations
from typing import Protocol, List, Tuple, Dict, Any, Optional
from pathlib import Path
from .models import (
    SecurityEvent,
    Evidence,
    EvidenceRelation,
    Hypothesis,
    CandidateAction,
    AgentDecision,
    ActionResult,
    TimelineEntry,
    InvestigationState,
    Investigation,
)


class IEventIngester(Protocol):
    """عقد وحدة استيراد البيانات — Member 1"""
    def ingest(self, file_path: str) -> List[SecurityEvent]:
        """قراءة ملف CSV أو JSON وتحويله إلى أحداث أمنية موحدة"""
        ...

    def validate(self, events: List[SecurityEvent]) -> List[SecurityEvent]:
        """التحقق من سلامة البيانات واستبعاد المشوهة أو وضع علامة عليها"""
        ...


class ICorrelationEngine(Protocol):
    """عقد محرك ربط الأدلة — Member 2"""
    def correlate(self, events: List[SecurityEvent]) -> Tuple[List[Evidence], List[EvidenceRelation]]:
        """تطبيق قواعد الارتباط واستخراج الأدلة والعلاقات بدون افتراض السببية"""
        ...

    def build_graph(self, evidence: List[Evidence], relations: List[EvidenceRelation]) -> Any:
        """بناء NetworkX DiGraph وتمثيله للتحليل والعرض"""
        ...


class IHypothesisEngine(Protocol):
    """عقد محرك الفرضيات — Member 4"""
    def generate_hypotheses(self, evidence: List[Evidence]) -> List[Hypothesis]:
        """توليد الفرضيات الأولية وتحديد الأدلة الناقصة المطلوبة"""
        ...

    def update_hypothesis(self, hypothesis: Hypothesis, new_evidence: List[Evidence]) -> Hypothesis:
        """تحديث درجة الثقة وتغيير الحالة (OPEN, SUPPORTED, WEAKENED, REJECTED, CONFIRMED)"""
        ...


class ITimelineBuilder(Protocol):
    """عقد بناء الخط الزمني — Member 4"""
    def build_timeline(
        self,
        events: List[SecurityEvent],
        evidence: List[Evidence],
        decisions: List[AgentDecision]
    ) -> List[TimelineEntry]:
        """دمج الأحداث والأدلة وقرارات الوكيل في خط زمني تسلسلي واضح"""
        ...


class IAgentCore(Protocol):
    """عقد نواة الوكيل الذكي — Member 3"""
    def perceive(self, events: List[SecurityEvent]) -> InvestigationState:
        """استقبال الأحداث الجديدة وتحديث الكيانات والحالة الأولية"""
        ...

    def reason(self, state: InvestigationState) -> List[CandidateAction]:
        """توليد الإجراءات المرشحة وحساب منفعتها U(a) = B(a) - C(a) - R(a) وترتيبها"""
        ...

    def select_action(self, candidates: List[CandidateAction]) -> AgentDecision:
        """اختيار الإجراء ذي المنفعة القصوى وتوثيق أسباب الاختيار"""
        ...

    def execute(self, decision: AgentDecision) -> ActionResult:
        """تنفيذ الإجراء في بيئة المحاكاة الآمنة واستقبال التغذية الراجعة"""
        ...

    def update_state(self, state: InvestigationState, result: ActionResult) -> InvestigationState:
        """تحديث الحالة الداخلية للوكيل بناءً على التغذية الراجعة"""
        ...


class IStorage(Protocol):
    """عقد تخزين التحقيقات — Member 6 / Infrastructure"""
    def save_investigation(self, investigation: Investigation) -> str:
        ...

    def load_investigation(self, investigation_id: str) -> Optional[Investigation]:
        ...

    def list_investigations(self) -> List[Dict[str, Any]]:
        ...

    def save_decision(self, decision: AgentDecision, investigation_id: str) -> str:
        ...


class IReporter(Protocol):
    """عقد توليد التقارير — Member 5"""
    def generate_report(self, investigation: Investigation) -> Dict[str, Any]:
        """توليد ملخص تنفيذي وتقني للتحقيق قابل للتصدير"""
        ...
