"""
TraceMind — Central Configuration
جميع الأوزان والمعايير القابلة للضبط والمحاذاة في النظام.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CorrelationConfig:
    temporal_window_seconds: int = 3600       # ساعة واحدة كنافذة زمنية عامة
    short_window_seconds: int = 300          # 5 دقائق للأنماط المكثفة مثل Brute Force
    min_edge_confidence: float = 0.5         # حد أدنى لربط حافة
    same_account_weight: float = 0.90
    same_device_weight: float = 0.85
    network_relation_weight: float = 0.80
    same_indicator_weight: float = 0.95


@dataclass
class AgentConfig:
    # Benefit Weights w_B (مجموعها = 1.0)
    w_information_gain: float = 0.40         # تقليل عدم اليقين والمكسب المعلوماتي
    w_hypothesis_utility: float = 0.35       # الصلة بالفرضيات المفتوحة
    w_missing_evidence: float = 0.25         # قدرة الإجراء على جلب أدلة ناقصة حرجة

    # Cost Weights w_C (مجموعها = 1.0)
    w_records_processed: float = 0.50        # العبء الحسابي لعدد السجلات
    w_time_complexity: float = 0.50          # زمن انتظار البيانات

    # Risk Weights w_R (مجموعها = 1.0)
    w_false_escalation: float = 0.60         # خطر التصعيد دون أدلة حاسمة
    w_evidence_weakness: float = 0.40        # التكلفة المترتبة على أدلة غير موثوقة

    # Hyperparameters & Stopping Conditions
    max_investigation_steps: int = 20
    min_confidence_to_confirm: float = 0.85
    min_confidence_to_escalate: float = 0.75
    rejection_confidence_threshold: float = 0.20
    max_candidate_actions: int = 10


@dataclass
class AppConfig:
    project_root: Path = Path(__file__).parent.parent.parent
    db_path: Path = Path(__file__).parent.parent.parent / "data" / "tracemind.db"
    raw_data_dir: Path = Path(__file__).parent.parent.parent / "data" / "raw"
    normalized_data_dir: Path = Path(__file__).parent.parent.parent / "data" / "normalized"
    scenarios_dir: Path = Path(__file__).parent.parent.parent / "data" / "scenarios"
    correlation: CorrelationConfig = field(default_factory=CorrelationConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


config = AppConfig()
