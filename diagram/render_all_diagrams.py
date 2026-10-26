import os
import subprocess
import time
from pathlib import Path

# Setup directories
desktop_dir = Path(r"C:\Users\Click Labtop\Desktop")
docs_diagrams_dir = Path(r"C:\Users\Click Labtop\.gemini\antigravity\scratch\tracemind\docs\diagrams")
docs_diagrams_dir.mkdir(parents=True, exist_ok=True)
scratch_dir = Path(r"C:\Users\Click Labtop\.gemini\antigravity\scratch")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

diagrams = [
    {
        "filename": "01_System_Context_Diagram",
        "title": "1. المخطط المعماري للنظام (System Context Diagram)",
        "mermaid": """flowchart TB
    subgraph Users ["المستخدمون والمشرفون"]
        Analyst["محلل الحوادث السيبرانية / المحقق"]
    end

    subgraph PresentationLayer ["Presentation Layer (UI)"]
        StreamlitApp["Streamlit Dashboard & Visualizations\\n(Plotly Graphs, Timeline, Hypotheses)"]
    end

    subgraph ApplicationLayer ["Application Layer (Service Contracts)"]
        InvService["Investigation Orchestrator Service"]
        ActionExec["Action Execution & Simulation Engine"]
        ReportService["Reporting & Export Service"]
    end

    subgraph DomainLayer ["Domain Layer (Core Intelligence)"]
        direction TB
        SharedModels["Canonical Domain Models & DTOs\\n(SecurityEvent, Evidence, Hypothesis, State)"]
        IngestionMod["Data Ingestion & Normalizer (M1)"]
        CorrelationMod["Evidence Correlation Engine (NetworkX MultiDiGraph M2)"]
        HypothesisMod["Hypothesis & Timeline Engine (M4)"]
        AgentCoreMod["Intelligent Agent Core\\n(Pure Reasoning M3)"]
    end

    subgraph InfrastructureLayer ["Infrastructure Layer"]
        SQLiteDB[("SQLite Database\\nNormalized Storage")]
        Repositories["Investigation & Event Repositories (M1)"]
        FileIO["File Storage & Parser Drivers\\n(CSV / JSON Datasets)"]
    end

    Analyst -->|يتفاعل مع اللوحة والتقارير| StreamlitApp
    StreamlitApp -->|يستدعي الخدمات فقط| InvService
    StreamlitApp -->|يطلب التقارير| ReportService

    InvService --> IngestionMod
    InvService --> CorrelationMod
    InvService --> HypothesisMod
    InvService --> AgentCoreMod
    InvService --> ActionExec
    ActionExec -->|سجلات محاكاة جديدة RawLogPayload| IngestionMod
    InvService --> Repositories
    Repositories --> SQLiteDB

    IngestionMod -->|يقرأ السجلات| FileIO
    CorrelationMod --> SharedModels
    HypothesisMod --> SharedModels
    AgentCoreMod --> SharedModels

    ReportService --> SQLiteDB"""
    },
    {
        "filename": "02_Component_Architecture",
        "title": "2. معمارية المكونات وتدفق البيانات (Component Architecture)",
        "mermaid": """flowchart LR
    subgraph Ingestion ["1. وحدة الاستيراد والتخزين (M1)"]
        CSVParser["CSV / JSON / Payload Parsers"]
        Normalizer["Event Normalizer"]
        Deduplicator["Deduplication Engine"]
        Repos["SQLite Repositories"]
    end

    subgraph Correlation ["2. محرك الارتباط (M2)"]
        Rules["Correlation Rules Engine"]
        NetXGraph["NetworkX MultiDiGraph"]
    end

    subgraph Investigation ["3. محرك الفرضيات والخط الزمني (M4)"]
        HypoTracker["Hypothesis State Tracker"]
        TimelineGen["Timeline Generator"]
    end

    subgraph Agent ["4. نواة الوكيل الذكي (M3)"]
        Perception["Perception Filter"]
        UtilityCalc["Utility Engine: U(a)"]
        Explainer["Decision Explainer"]
    end

    subgraph AppOrch ["Application Orchestrator (M6)"]
        Orchestrator["Workflow Controller"]
        SimRunner["Action Simulation Runner"]
    end

    Ingestion -->|SecurityEvents موحدة| Correlation
    Correlation -->|Evidence + Relations| Investigation
    Investigation -->|State + Missing Info| Orchestrator
    Orchestrator -->|Current State| Agent
    Agent -->|AgentDecision فقط| Orchestrator
    Orchestrator -->|Selected Action| SimRunner
    SimRunner -->|ActionExecutionResponse\\n(RawLogPayloads)| Ingestion"""
    },
    {
        "filename": "03_Data_Flow_Sequence",
        "title": "3. مخطط تدفق البيانات التسلسلي (End-to-End Sequence Diagram)",
        "mermaid": """sequenceDiagram
    autonumber
    actor User as المحلل السيبراني
    participant UI as Streamlit UI
    participant Orch as InvestigationOrchestrator
    participant Ing as Ingestion Engine (M1)
    participant Cor as Correlation Engine (M2)
    participant Hyp as Hypothesis Engine (M4)
    participant Agt as Agent Core (M3)
    participant Sim as ActionExecutionEngine
    participant DB as SQLite Storage (M1)

    User->>UI: بدء تحقيق جديد واختيار السجلات
    UI->>Orch: start_investigation(files)
    Orch->>Ing: ingest_file(files)
    Ing-->>Orch: IngestionResult (events)
    Orch->>Cor: correlate(events)
    Cor-->>Orch: CorrelationResult (evidence, relations, MultiDiGraph)
    Orch->>Hyp: generate_initial_hypotheses(evidence)
    Hyp-->>Orch: List[Hypothesis] + missing_information
    Orch->>DB: save_state(InvestigationState)

    rect rgb(240, 248, 255)
        Note over Orch,Sim: حلقة اتخاذ القرار الوكيلاتي المنفصلة (Decoupled Agent Loop)
        Orch->>Agt: evaluate_and_decide(state)
        Note over Agt: 1. Generate Candidates<br/>2. Score U(a) = B - C - R<br/>3. Select Best<br/>4. Generate Explanation
        Agt-->>Orch: AgentDecision (Selected Action)
        
        Orch->>DB: record_decision(AgentDecision)
        Note over DB: حفظ القرار والخيارات وقيد uq_selected_candidate_per_decision
        
        Orch->>Sim: execute_action(selected_action)
        Note over Sim: جلب السجلات المحاكاة للجهاز الهدف
        Sim-->>Orch: ActionExecutionResponse (action_result, raw_payloads)
        
        loop لكل حمولة سجلات جديدة
            Orch->>Ing: ingest_payload(payload)
            Ing-->>Orch: IngestionResult (new_events)
            Orch->>Cor: correlate(new_events)
            Cor-->>Orch: New Evidence & MultiDiGraph Edges
        end
        
        Orch->>Hyp: update_hypotheses(new_evidence)
        Hyp-->>Orch: Updated Hypotheses & Confidence
    end

    Orch->>DB: save_state(updated_state)
    Orch-->>UI: InvestigationSummary
    UI-->>User: عرض الخط الزمني، شبكة الأدلة، التفسيرات، والتوصيات"""
    },
    {
        "filename": "04_Domain_Model_Class_Diagram",
        "title": "4. مخطط الكيانات والمخطط المفاهيمي (Domain Model Class Diagram)",
        "mermaid": """classDiagram
    class SecurityEvent {
        +str id
        +datetime timestamp
        +EventType event_type
        +Severity severity
        +str source_file
        +ValidationStatus validation_status
        +Optional[str] account_id
        +Optional[str] device_id
        +Optional[str] source_ip
        +Optional[str] destination_ip
        +Optional[str] indicator
        +dict raw_data
        +datetime normalized_at
    }

    class Evidence {
        +str id
        +EvidenceType evidence_type
        +str source_event_id
        +float reliability
        +str observed_value
        +datetime timestamp
        +str provenance
    }

    class EvidenceRelation {
        +str id
        +str source_evidence_id
        +str target_evidence_id
        +RelationType relation_type
        +float weight
        +float confidence
        +Optional[float] temporal_delta_seconds
        +str provenance
        +datetime created_at
    }

    class Hypothesis {
        +str id
        +str description
        +HypothesisStatus status
        +float confidence
        +List[str] missing_evidence_types
        +datetime created_at
        +datetime updated_at
    }

    class CandidateAction {
        +str id
        +Optional[str] decision_id
        +ActionType action_type
        +Optional[str] target_entity
        +str description
        +float estimated_benefit
        +float estimated_cost
        +float estimated_risk
        +float utility
        +bool is_selected
        +dict parameters
    }

    class AgentDecision {
        +str id
        +CandidateAction selected_action
        +List[CandidateAction] candidate_actions
        +float utility_score
        +str explanation
        +int investigation_step
        +datetime timestamp
    }

    class RawLogPayload {
        +str source_name
        +str format
        +str content
        +dict metadata
    }

    class ActionExecutionResponse {
        +ActionResult action_result
        +List[RawLogPayload] raw_payloads
    }

    SecurityEvent "1" <-- "1..*" Evidence : generates
    Evidence "1" <-- "0..*" EvidenceRelation : source_node
    Evidence "1" <-- "0..*" EvidenceRelation : target_node
    Hypothesis "1" -- "0..*" Evidence : associations
    AgentDecision "1" *-- "1" CandidateAction : selected (is_selected=True)
    AgentDecision "1" *-- "0..*" CandidateAction : alternatives (is_selected=False)
    AgentDecision "1" <-- "1" ActionExecutionResponse : produces response
    ActionExecutionResponse *-- "1" ActionResult
    ActionExecutionResponse *-- "0..*" RawLogPayload"""
    },
    {
        "filename": "05_Hypothesis_State_Lifecycle",
        "title": "5. دورة حياة الفرضية (Hypothesis State Lifecycle)",
        "mermaid": """stateDiagram-v2
    [*] --> OPEN: تكوين الفرضية بناءً على مؤشرات مبدئية
    OPEN --> SUPPORTED: ورود أدلة مؤيدة إضافية (Confidence > 0.60)
    OPEN --> WEAKENED: ورود أدلة معارضة أو نقص شديد (Confidence < 0.40)
    SUPPORTED --> ESCALATED: اكتمال الأدلة وارتفاع الثقة (Confidence >= 0.75)
    SUPPORTED --> CONFIRMED: تأكيد قطعي بوجود أدلة حاسمة غير قابلة للشك (Confidence >= 0.85)
    WEAKENED --> REJECTED: إثبات عدم صحة الفرضية بوجود أدلة نافية قاطعة (Confidence <= 0.20)
    CONFIRMED --> [*]
    REJECTED --> [*]
    ESCALATED --> [*]: تحويل القرار للتدخل البشري"""
    },
    {
        "filename": "06_SQLite_ERD_Diagram",
        "title": "6. مخطط الكيانات والعلاقات لقاعدة البيانات (SQLite Database ERD)",
        "mermaid": """erDiagram
    INVESTIGATIONS ||--o{ SECURITY_EVENTS : contains
    INVESTIGATIONS ||--o{ EVIDENCE : contains
    INVESTIGATIONS ||--o{ EVIDENCE_RELATIONS : contains
    INVESTIGATIONS ||--o{ HYPOTHESES : tracks
    INVESTIGATIONS ||--o{ AGENT_DECISIONS : logs
    INVESTIGATIONS ||--o{ TIMELINE_ENTRIES : contains

    SECURITY_EVENTS ||--o{ EVIDENCE : generates
    EVIDENCE ||--o{ EVIDENCE_RELATIONS : source_node
    EVIDENCE ||--o{ EVIDENCE_RELATIONS : target_node

    HYPOTHESES ||--o{ HYPOTHESIS_EVIDENCE : associations
    EVIDENCE ||--o{ HYPOTHESIS_EVIDENCE : linked_evidence

    AGENT_DECISIONS ||--o{ CANDIDATE_ACTIONS : evaluated_options
    AGENT_DECISIONS ||--o| ACTION_RESULTS : dispatches

    AGENT_DECISIONS {
        text id PK
        text investigation_id FK
        integer step_number
        text selected_action_id FK
        real utility_score
        real benefit
        real cost
        real risk
        text explanation
        text timestamp
    }

    CANDIDATE_ACTIONS {
        text id PK
        text decision_id FK
        text action_type
        text target_entity
        text description
        real estimated_benefit
        real estimated_cost
        real estimated_risk
        real utility
        integer is_selected
        text parameters_json
    }

    ACTION_RESULTS {
        text id PK
        text decision_id FK
        integer success
        text feedback_message
        integer simulated
        text timestamp
    }"""
    },
    {
        "filename": "07_Agent_Decision_Loop",
        "title": "7. دورة اتخاذ القرار واستدلال الوكيل (Agent Decision Loop)",
        "mermaid": """flowchart TD
    Start([بدء التحقيق أو استقبال بيانات جديدة]) --> Perception[1. الإدراك والتصفية Perception]
    Perception --> UpdateState[2. تحديث الكيانات والحالة الداخلية State Update]
    UpdateState --> EvalHypo[3. تقييم الفرضيات وكشف النقص والمنافاة]
    EvalHypo --> GenActions[4. توليد الإجراءات المرشحة Candidate Generation]
    GenActions --> CalcUtility[5. حساب المنفعة: U = Benefit - Cost - Risk]
    CalcUtility --> SelectBest[6. اختيار الإجراء الأعلى منفعة وضبط is_selected=True]
    SelectBest --> GenExplanation[7. توليد التفسير المنطقي Explanation]
    GenExplanation --> EmitDecision([إصدار كائن AgentDecision إلى طبقة التنسيق])"""
    },
    {
        "filename": "08_Evidence_Correlation_Graph",
        "title": "8. شبكة ارتباط الأدلة في NetworkX (MultiDiGraph Example)",
        "mermaid": """graph LR
    E1["Event 1: Failed Login<br/>User: Alice | WS-001<br/>02:15:00"]
    E2["Event 2: Failed Login<br/>User: Alice | WS-001<br/>02:15:05"]
    E3["Event 3: Success Login<br/>User: Alice | WS-001<br/>02:15:40"]
    E4["Event 4: Outbound Connection<br/>From: WS-001 To: SRV-002<br/>02:16:10"]

    E1 -->|SAME_ACCOUNT<br/>Weight: 0.95| E2
    E1 -.->|TEMPORALLY_RELATED<br/>Weight: 0.98| E2
    E2 -->|SAME_ACCOUNT<br/>Weight: 0.95| E3
    E3 -->|SAME_DEVICE<br/>Weight: 0.90| E4"""
    },
    {
        "filename": "09_Team_Dependency_Graph",
        "title": "9. مخطط التبعيات والتوازي للمطورين الستة (Team Dependency Graph)",
        "mermaid": """flowchart TD
    M6_Models["Member 6: النماذج والعقود الموحدة\\n(Shared Domain Models & Protocols)"]
    
    subgraph ParallelPhase1 ["مرحلة التطوير المستقل (الأسبوع 1 و 2 عبر الـ Mocks)"]
        M1_Ingestion["Member 1: معالجة السجلات واستيعاب الحمولات ومستودعات SQLite"]
        M2_Correlation["Member 2: محرك الارتباط وقواعد MultiDiGraph"]
        M4_Hypothesis["Member 4: إدارة الفرضيات والخط الزمني"]
        M3_Agent["Member 3: دالة المنفعة واستدلال الوكيل النقي"]
        M5_UI["Member 5: واجهات Streamlit و Plotly (بيانات تجريبية)"]
    end

    subgraph IntegrationPhase ["مرحلة التكامل المتتابع (نهاية الأسبوع 2 و 3)"]
        Int_1["تكامل Ingestion مع Correlation (M1 -> M2)"]
        Int_2["تكامل Correlation مع Hypotheses (M2 -> M4)"]
        Int_3["تكامل Hypotheses مع Agent Core (M4 -> M3)"]
        Int_4["ربط الوكيل بخدمة المحاكاة والتنسيق وقاعدة البيانات (M3 -> M6)"]
        Int_5["ربط واجهة Streamlit بالخدمة الكاملة (M5 -> M6)"]
    end

    M6_Models --> M1_Ingestion
    M6_Models --> M2_Correlation
    M6_Models --> M4_Hypothesis
    M6_Models --> M3_Agent
    M6_Models --> M5_UI

    M1_Ingestion --> Int_1
    M2_Correlation --> Int_1
    Int_1 --> Int_2
    M4_Hypothesis --> Int_2
    Int_2 --> Int_3
    M3_Agent --> Int_3
    Int_3 --> Int_4
    Int_4 --> Int_5
    M5_UI --> Int_5"""
    },
    {
        "filename": "10_Testing_Pyramid",
        "title": "10. هرم وتوزيع اختبارات النظام (Testing Strategy Pyramid)",
        "mermaid": """pie title هرم الاختبارات لمشروع TraceMind
    "Unit Tests (اختبارات الوحدات المعزولة)": 70
    "Integration Tests (اختبارات التكامل بين المكونات)": 20
    "End-to-End Scenarios (سيناريوهات التحقيق الشاملة)": 10"""
    },
    {
        "filename": "11_Four_Week_Roadmap",
        "title": "11. الخطة التنفيذية لـ 4 أسابيع (Four-Week Roadmap)",
        "mermaid": """gantt
    title خطة التنفيذ لستة مطورين (TraceMind 4-Week Schedule)
    dateFormat  YYYY-MM-DD
    section Week 1 (البنية والعقود)
    إعداد المستودع ونماذج البيانات المشتركة (M6) :w1_1, 2026-11-01, 3d
    تجهيز السيناريوهات الاصطناعية و CSV/JSON (M1) :w1_2, 2026-11-01, 5d
    هيكل قواعد الارتباط و MultiDiGraph (M2) :w1_3, 2026-11-03, 4d
    هيكل دورة حياة الفرضيات والخط الزمني (M4) :w1_4, 2026-11-03, 4d
    صياغة نموذج الحالة ودالة المنفعة للوكيل (M3) :w1_5, 2026-11-03, 4d
    هيكل واجهة Streamlit مع بيانات تجريبية (M5) :w1_6, 2026-11-04, 3d
    
    section Week 2 (المنطق الأساسي)
    تطوير Ingestion الكامل والتنظيف ومستودعات SQLite (M1) :w2_1, 2026-11-08, 5d
    تطوير قواعد محرك الارتباط وحساب الأوزان (M2) :w2_2, 2026-11-08, 5d
    تطوير محرك الفرضيات ومعادلة الثقة (M4) :w2_3, 2026-11-08, 5d
    تطوير استدلال الوكيل وتوليد الإجراءات U(a) (M3) :w2_4, 2026-11-08, 5d
    تطوير صفحات الخط الزمني واستكشاف الأدلة (M5) :w2_5, 2026-11-08, 5d
    بناء مخطط SQLite وتنسيق ActionExecutionResponse (M6) :w2_6, 2026-11-08, 5d

    section Week 3 (التكامل وحلقة الوكيل)
    ربط الاستيراد مع الارتباط وتغذية الأدلة (M1+M2) :w3_1, 2026-11-15, 4d
    تشغيل حلقة الوكيل الكاملة واستقبال التغذية (M3+M4+M6) :w3_2, 2026-11-15, 5d
    ربط واجهة Streamlit بالخدمات الحقيقية (M5) :w3_3, 2026-11-17, 4d
    تفعيل التخزين الدائم في SQLite لكافة الحركات (M1+M6) :w3_4, 2026-11-15, 5d

    section Week 4 (الاختبارات الشاملة والعرض)
    تنفيذ اختبارات E2E على السيناريوهات المرجعية (M6) :w4_1, 2026-11-22, 4d
    تحسين الشرح والتعليل وإحكام شروط التوقف (M3) :w4_2, 2026-11-22, 3d
    تحسين مظهر الرسوم البيانية وتوليد التقارير (M5) :w4_3, 2026-11-23, 3d
    التوثيق النهائي، تقرير المشروع، وتحضير العرض التوضيحي (الجميع) :w4_4, 2026-11-25, 4d"""
    },
    {
        "filename": "12_First_Vertical_Slice",
        "title": "12. الشريحة الرأسية الأولى (First Vertical Slice)",
        "mermaid": """flowchart LR
    CSV["ملف CSV مصغر (3 أحداث: 2 فشل + 1 نجاح)"] --> Ingest["استيراد وتطبيع"]
    Ingest --> Correlate["ربط SAME_ACCOUNT"]
    Correlate --> Hypo["توليد فرضية Brute Force بنسبة ثقة 0.65"]
    Hypo --> Agent["حساب المنفعة لاختيار طلب سجلات إضافية"]
    Agent --> Decision["اتخاذ قرار توليد التفسير"]
    Decision --> UI["عرض النتيجة في جدول Streamlit مبسط"]"""
    }
]

# Render each diagram to PNG in both docs/diagrams and Desktop/TraceMind_Diagrams
desktop_images_dir = desktop_dir / "TraceMind_Diagrams"
desktop_images_dir.mkdir(parents=True, exist_ok=True)

for idx, d in enumerate(diagrams, 1):
    single_html_path = scratch_dir / f"diagram_{idx}.html"
    docs_png = docs_diagrams_dir / f"{d['filename']}.png"
    desktop_png = desktop_images_dir / f"{d['filename']}.png"
    
    single_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{ useMaxWidth: false }},
            sequence: {{ useMaxWidth: false }}
        }});
    </script>
    <style>
        body {{
            background-color: white;
            margin: 0;
            padding: 30px;
            display: inline-block;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .title {{
            font-size: 22px;
            font-weight: bold;
            color: #1e3a8a;
            margin-bottom: 20px;
            direction: rtl;
            font-family: sans-serif;
        }}
        .mermaid {{
            background: white;
        }}
    </style>
</head>
<body>
    <div class="title">{d['title']}</div>
    <div class="mermaid">
{d['mermaid']}
    </div>
</body>
</html>"""
    
    with open(single_html_path, "w", encoding="utf-8") as f:
        f.write(single_html)
        
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={docs_png}",
        "--window-size=1800,1200",
        "--virtual-time-budget=3000",
        f"file:///{single_html_path}"
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Also copy to desktop folder
        import shutil
        shutil.copyfile(docs_png, desktop_png)
        print(f"[{idx}/12] Re-rendered PNG: {d['filename']}.png ({docs_png.stat().st_size} bytes)")
    except Exception as e:
        print(f"[{idx}/12] Error rendering {d['filename']}: {e}")

print("All diagram assets re-rendered and updated successfully!")
