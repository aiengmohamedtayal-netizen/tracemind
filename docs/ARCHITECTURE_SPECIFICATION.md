# TraceMind — وثيقة التصميم المعماري وخطة التنفيذ (Architecture & Planning Specification)

---

## 1. Requirements Analysis (تحليل المتطلبات والافتراضات)

### 1.1 طبيعة النظام وسياق المشروع
مشروع **TraceMind** هو نظام ذكي تفاعلي لإدارة وتحليل التحقيقات في الحوادث السيبرانية (Intelligent Cyber Incident Investigator). صُمم المشروع في سياق أكاديمي لمقرر **Intelligent Agents**، بهدف إثبات السلوك الوكيلاتي الكامل (Agency) عبر دورة حياة متسلسلة تشمل:
$$\text{Perception} \to \text{Internal State} \to \text{Reasoning} \to \text{Planning} \to \text{Action} \to \text{Feedback}$$

النظام لا يعمل كأداة مراقبة تقليدية (Rule-Based SIEM) تعتمد فقط على تنبيهات جامدة مثل (`if failed_logins > 5: alert()`)، بل يمتلك **حالة داخلية تراكمية** للتحقيق، ويدير **فرضيات متعددة متنافسة**، ويحسب **منفعة جمع المعلومات الإضافية** عبر دالة منفعة واضحة:
$$U(a) = B(a) - C(a) - R(a)$$

### 1.2 المتطلبات الوظيفية الأساسية (Functional Requirements)
1. **استيعاب السجلات (Log Ingestion & Parsing):**
   - قراءة السجلات بتنسيقات CSV و JSON.
   - التحقق من سلامة البيانات واكتشاف السجلات التالفة والتكرارات (Deduplication).
   - توحيد الأحداث وفق نموذج بيانات قياسي موحد (`SecurityEvent`).
2. **ربط الأدلة (Evidence Correlation):**
   - ربط الأحداث وفق محاور: الحساب (`account_id`)، الجهاز (`device_id`)، الوقت (التقارب الزمني)، وعناوين الشبكة والمؤشرات المشتركة (`Indicators`).
   - بناء رسم بياني موجّه للأدلة (`Evidence Graph`) باستخدام مكتبة NetworkX.
   - الفصل الصارم بين الارتباط والسببية: $(\text{Correlation} \neq \text{Causation})$.
3. **إدارة الفرضيات (Hypothesis Management):**
   - صياغة فرضيات أولية متعددة (مثل: *Brute Force Attack*, *Lateral Movement*, *Normal IT Admin Activity*).
   - ربط الأدلة الداعمة (`Supporting Evidence`) والأدلة النافية/المعارضة (`Contradicting Evidence`).
   - تحديد الأدلة المفقودة (`Missing Information`) المطلوبة لحسم كل فرضية.
   - تحديث مستوى الثقة بالفرضية ديناميكياً وفق الأدلة الواردة.
4. **نواة الوكيل الذكي (Intelligent Agent Core):**
   - توليد إجراءات تحقيق مرشحة (`Candidate Actions`) مثل: طلب سجلات إضافية لجهاز معين، تحليل حدث مرتبط، التحقيق في كيان، أو تصعيد الحادث للمراجعة البشرية.
   - تقييم الإجراءات بناءً على دالة المنفعة الرياضية $U(a) = B(a) - C(a) - R(a)$.
   - تنفيذ الإجراء في بيئة محاكاة آمنة (Simulated Execution) وتلقي التغذية الراجعة.
   - توفير تفسير شفاف لكل قرار (`Decision Explainability`) يربط القرار بالأدلة والحسابات.
5. **الخط الزمني الموحد (Timeline Reconstruction):**
   - بناء تسلسل زمني دقيق يجمع: الأحداث المكتشفة، الأدلة المستنتجة، قرارات الوكيل، والتغذية الراجعة.
6. **واجهة المستخدم والتقارير (Streamlit Dashboard & Reporting):**
   - لوحة تحكم تفاعلية توفر نظرة عامة على التحقيقات، استكشاف الأحداث، رسم شبكة الأدلة (Plotly)، الخط الزمني، شجرة الفرضيات، وسجل قرارات الوكيل.
   - عزل تام لمنطق العمل: الواجهة تستهلك خدمات (`Services`) فقط ولا تتضمن قواعد منطقية داخلية.

### 1.3 المتطلبات غير الوظيفية (Non-Functional Requirements)
- **الأمان المطلق (Safety & Sandboxing):** تشغيل النظام بالكامل على بيانات محاكاة مصرح بها، وعدم تنفيذ أي إجراء هجومي أو تعديل على أنظمة إنتاجية حقيقية.
- **القابلية للاختبار (Testability):** استقلالية الوكيل ونواة المنطق عن واجهة Streamlit وقاعدة البيانات لتسهيل اختبارات Unit و Integration عبر `pytest`.
- **قابلية التوازي (Parallelizability):** بنية معمارية تمكّن 6 مطورين من العمل معاً دون تضارب في الشيفرة البرمجية.
- **الحتمية والقابلية للتكرار (Determinism & Reproducibility):** إمكانية إعادة تشغيل نفس السيناريو والحصول على نفس القرارات وحسابات المنفعة.

---

## 2. System Architecture (معمارية النظام الشاملة)

### 2.1 تقييم واختيار النمط المعماري (Architecture Style Decision)
تمت المقارنة بين ثلاثة أنماط معمارية رئيسية لاختيار الأنسب لمشروع TraceMind:

| المعيار | Pure Monolith (كتلي بسيط) | Microservices (خدمات مصغرة) | **Modular Monolith (كتلي معياري - المختار)** |
| :--- | :--- | :--- | :--- |
| **التعقيد التشغيلي** | منخفض جداً | مرتفع جداً (شبكات، حاويات، مزامنة) | **منخفض ومثالي للبيئة المحلية** |
| **سرعة التطوير** | سريعة في البداية ثم تتباطأ | بطيئة جداً بسبب الـ Overhead | **سريعة وثابتة طوال الـ 4 أسابيع** |
| **توازي عمل 6 مطورين** | ضعيف (تضاربات دمج مستمرة) | ممتاز نظرياً، معقد عملياً | **ممتاز بفضل عقود Interfaces الواضحة** |
| **سهولة الاختبار** | متوسطة (تداخل المكونات) | صعبة (تتطلب Mocking للشبكة) | **ممتازة (Mocking عبر Protocols محلية)** |
| **التبعيات التقنية** | ملفات مكدسة بدون حدود | Docker, gRPC/HTTP, Message Queues | **Python + SQLite فقط (حسب المقترح)** |
| **الملاءمة الأكاديمية** | تفتقر للتنظيم الهندسي المتقدم | مبالغ فيها وتشتت عن منطق الوكيل | **الخيار المثالي هندسياً وأكاديمياً** |

> **القرار المعماري:** اعتماد **Modular Monolith** المقسم إلى طبقات نظيفة (Layered Domain-Driven Boundaries)، حيث تعمل جميع الوحدات داخل بيئة تشغيل Python واحدة ولكن بحدود صارمة تمنع التداخل المباشر إلا عبر عقود معرّفة (`Protocols/Contracts`).

### 2.2 المخطط المعماري للنظام (System Context Diagram)

```mermaid
flowchart TB
    subgraph Users ["المستخدمون والمشرفون"]
        Analyst["محلل الحوادث السيبرانية / المستخدم"]
    end

    subgraph PresentationLayer ["Presentation Layer (UI)"]
        StreamlitApp["Streamlit Dashboard & Visualizations\n(Plotly Graphs, Timeline, Hypotheses)"]
    end

    subgraph ApplicationLayer ["Application Layer (Service Contracts)"]
        InvService["Investigation Orchestrator Service"]
        ReportService["Reporting & Export Service"]
    end

    subgraph DomainLayer ["Domain Layer (Core Intelligence)"]
        direction TB
        SharedModels["Canonical Domain Models\n(SecurityEvent, Evidence, Hypothesis, State)"]
        IngestionMod["Data Ingestion & Normalizer"]
        CorrelationMod["Evidence Correlation Engine (NetworkX)"]
        HypothesisMod["Hypothesis & Timeline Engine"]
        AgentCoreMod["Intelligent Agent Core\n(Perception → Reasoning → Utility → Action)"]
    end

    subgraph InfrastructureLayer ["Infrastructure Layer"]
        SQLiteDB[(SQLite Database\nStorage Engine)]
        FileIO["File Storage & Parser Drivers\n(CSV / JSON Datasets)"]
    end

    Analyst -->|يتفاعل مع اللوحة والتقارير| StreamlitApp
    StreamlitApp -->|يستدعي الخدمات فقط| InvService
    StreamlitApp -->|يطلب التقارير| ReportService

    InvService --> IngestionMod
    InvService --> CorrelationMod
    InvService --> HypothesisMod
    InvService --> AgentCoreMod
    InvService -->|يحفظ ويسترجع الحالة| SQLiteDB

    IngestionMod -->|يقرأ السجلات| FileIO
    CorrelationMod --> SharedModels
    HypothesisMod --> SharedModels
    AgentCoreMod --> SharedModels

    ReportService --> SQLiteDB
```

---

## 3. Component Architecture (معمارية المكونات وتدفق البيانات)

### 3.1 توصيف المكونات الرئيسية ومسؤولياتها

```mermaid
flowchart LR
    subgraph Ingestion ["1. وحدة الاستيراد"]
        CSVParser["CSV / JSON Parsers"]
        Normalizer["Event Normalizer"]
        Deduplicator["Deduplication Engine"]
    end

    subgraph Correlation ["2. محرك الارتباط"]
        Rules["Correlation Rules Engine"]
        NetXGraph["NetworkX Evidence Graph"]
    end

    subgraph Investigation ["3. محرك الفرضيات والخط الزمني"]
        HypoTracker["Hypothesis State Tracker"]
        TimelineGen["Timeline Generator"]
    end

    subgraph Agent ["4. نواة الوكيل الذكي"]
        Perception["Perception Filter"]
        UtilityCalc["Utility Engine: U(a)"]
        ActionSim["Simulated Action Runner"]
        Explainer["Decision Explainer"]
    end

    Ingestion -->|SecurityEvents موحدة| Correlation
    Correlation -->|Evidence + Relations| Investigation
    Investigation -->|State + Missing Info| Agent
    Agent -->|Simulated Action| Ingestion
    Agent -->|Decisions & Feedback| Investigation
```

### 3.2 مخطط تدفق البيانات التسلسلي (End-to-End Data Flow Sequence)

```mermaid
sequenceDiagram
    autonumber
    actor User as المحقق / المستخدم
    participant UI as Streamlit UI
    participant Svc as InvestigationService
    participant Ing as Ingestion Engine (M1)
    participant Cor as Correlation Engine (M2)
    participant Hyp as Hypothesis Engine (M4)
    participant Agt as Agent Core (M3)
    participant DB as SQLite Storage (M6)

    User->>UI: بدء تحقيق جديد واختيار السجلات
    UI->>Svc: start_investigation(files)
    Svc->>Ing: ingest_and_normalize(files)
    Ing-->>Svc: List[SecurityEvent]
    Svc->>Cor: correlate(events)
    Cor-->>Svc: Tuple[List[Evidence], List[EvidenceRelation], NetworkX Graph]
    Svc->>Hyp: generate_initial_hypotheses(evidence)
    Hyp-->>Svc: List[Hypothesis] + missing_information
    Svc->>Agt: initialize_state(events, evidence, hypotheses)
    Agt-->>Svc: InvestigationState (Step 0)
    Svc->>DB: save_state(InvestigationState)

    rect rgb(240, 245, 255)
        Note over Svc,Agt: حلقة اتخاذ القرار الوكيلاتي (Agent Loop)
        Svc->>Agt: plan_and_select_action(InvestigationState)
        Agt->>Agt: Evaluate Candidate Actions via U(a) = B - C - R
        Agt->>Agt: Generate Explanation
        Agt-->>Svc: AgentDecision (Action: REQUEST_ADDITIONAL_LOGS)
        Svc->>Agt: execute_simulated_action(AgentDecision)
        Agt-->>Svc: ActionResult (New Simulated Logs Discovered)
        Svc->>Ing: parse_additional_logs(new_source)
        Ing-->>Svc: List[SecurityEvent] (New)
        Svc->>Cor: correlate_incremental(new_events)
        Cor-->>Svc: New Evidence & Relations
        Svc->>Hyp: update_hypotheses(new_evidence)
        Hyp-->>Svc: Updated Hypotheses & Confidence
        Svc->>Agt: update_internal_state(new_evidence, updated_hypotheses)
    end

    Svc->>DB: save_decision_and_state()
    Svc-->>UI: Complete Investigation Summary
    UI-->>User: عرض الخط الزمني، شبكة الأدلة، التفسيرات، والتوصيات
```

---

## 4. Domain Model (النموذج المجالي والمفاهيمي الموحد)

لضمان عدم حدوث تضارب بين المطورين الستة، يُمثّل النموذج المجالي **العقد المعياري المشترك** الذي تُبنى عليه كافة الوحدات.

### 4.1 الكيانات والمخطط المفاهيمي

```mermaid
classDiagram
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
        +List[str] related_evidence_ids
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
        +List[str] supporting_evidence_ids
        +List[str] contradicting_evidence_ids
        +List[str] missing_evidence_types
        +List[dict] history
        +datetime created_at
        +datetime updated_at
        +record_transition(new_status, new_conf, reason)
    }

    class CandidateAction {
        +str id
        +ActionType action_type
        +Optional[str] target_entity
        +str description
        +float estimated_benefit
        +float estimated_cost
        +float estimated_risk
        +float utility
        +dict parameters
        +compute_utility() float
    }

    class AgentDecision {
        +str id
        +CandidateAction selected_action
        +List[CandidateAction] candidate_actions
        +float utility_score
        +float benefit
        +float cost
        +float risk
        +List[str] evidence_ids_used
        +List[str] hypothesis_ids_considered
        +str explanation
        +int investigation_step
        +datetime timestamp
    }

    class ActionResult {
        +str id
        +str decision_id
        +bool success
        +List[str] new_evidence_ids
        +str feedback_message
        +bool simulated
        +datetime timestamp
    }

    class TimelineEntry {
        +str id
        +datetime timestamp
        +str entry_type
        +str title
        +str description
        +List[str] event_ids
        +List[str] evidence_ids
        +List[str] hypothesis_ids
        +Optional[str] decision_id
        +Optional[Severity] severity
    }

    class InvestigationState {
        +str investigation_id
        +List[Evidence] current_evidence
        +List[Hypothesis] hypotheses
        +List[TimelineEntry] timeline
        +dict known_entities
        +List[str] missing_information
        +List[CandidateAction] candidate_actions
        +List[CandidateAction] previous_actions
        +List[AgentDecision] decision_history
        +int current_step
        +InvestigationStatus status
        +datetime created_at
        +datetime updated_at
    }

    SecurityEvent "1" <-- "1..*" Evidence : derived from
    Evidence "1" <-- "0..*" EvidenceRelation : source / target
    Evidence "0..*" <-- "1" Hypothesis : supporting / contradicting
    InvestigationState "1" *-- "0..*" Evidence
    InvestigationState "1" *-- "0..*" Hypothesis
    InvestigationState "1" *-- "0..*" TimelineEntry
    InvestigationState "1" *-- "0..*" AgentDecision
    AgentDecision "1" *-- "1" CandidateAction : selected
    AgentDecision "1" <-- "1" ActionResult : generates feedback
```

### 4.2 دورة حياة الفرضية (Hypothesis State Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> OPEN: تكوين الفرضية بناءً على مؤشرات مبدئية
    OPEN --> SUPPORTED: ورود أدلة مؤيدة إضافية (Confidence > 0.60)
    OPEN --> WEAKENED: ورود أدلة معارضة أو نقص شديد (Confidence < 0.40)
    SUPPORTED --> ESCALATED: اكتمال الأدلة وارتفاع الثقة (Confidence >= 0.75)
    SUPPORTED --> CONFIRMED: تأكيد قطعي بوجود أدلة حاسمة غير قابلة للشك (Confidence >= 0.85)
    WEAKENED --> REJECTED: إثبات عدم صحة الفرضية بوجود أدلة نافية قاطعة (Confidence <= 0.20)
    CONFIRMED --> [*]
    REJECTED --> [*]
    ESCALATED --> [*]: تحويل القرار للتدخل البشري
```

---

## 5. Data Model (مخطط قاعدة بيانات SQLite والـ ERD)

تم اختيار SQLite كقاعدة بيانات محلية تلبي المتطلبات الأكاديمية الخفيفة وتسمح بتخزين واسترجاع التحقيقات دون الحاجة لخوادم خارجية.

```mermaid
erDiagram
    INVESTIGATIONS ||--o{ SECURITY_EVENTS : contains
    INVESTIGATIONS ||--o{ EVIDENCE : contains
    INVESTIGATIONS ||--o{ EVIDENCE_RELATIONS : contains
    INVESTIGATIONS ||--o{ HYPOTHESES : contains
    INVESTIGATIONS ||--o{ AGENT_DECISIONS : logs
    INVESTIGATIONS ||--o{ TIMELINE_ENTRIES : orders
    AGENT_DECISIONS ||--|| CANDIDATE_ACTIONS : selects
    AGENT_DECISIONS ||--o| ACTION_RESULTS : produces
    EVIDENCE ||--o{ EVIDENCE_RELATIONS : links

    INVESTIGATIONS {
        text id PK
        text name
        text description
        text status
        text source_files
        text created_at
        text updated_at
    }

    SECURITY_EVENTS {
        text id PK
        text investigation_id FK
        text timestamp
        text event_type
        text severity
        text source_file
        text validation_status
        text account_id
        text device_id
        text source_ip
        text destination_ip
        text indicator
        text raw_data
        text normalized_at
    }

    EVIDENCE {
        text id PK
        text investigation_id FK
        text evidence_type
        text source_event_id
        real reliability
        text observed_value
        text timestamp
        text provenance
        text related_evidence_ids
    }

    EVIDENCE_RELATIONS {
        text id PK
        text investigation_id FK
        text source_evidence_id FK
        text target_evidence_id FK
        text relation_type
        real weight
        real confidence
        real temporal_delta_seconds
        text provenance
        text created_at
    }

    HYPOTHESES {
        text id PK
        text investigation_id FK
        text description
        text status
        real confidence
        text supporting_evidence_ids
        text contradicting_evidence_ids
        text missing_evidence_types
        text history
        text created_at
        text updated_at
    }

    AGENT_DECISIONS {
        text id PK
        text investigation_id FK
        integer investigation_step
        text selected_action_id FK
        real utility_score
        real benefit
        real cost
        real risk
        text evidence_ids_used
        text hypothesis_ids_considered
        text explanation
        text timestamp
    }

    ACTION_RESULTS {
        text id PK
        text decision_id FK
        integer success
        text new_evidence_ids
        text feedback_message
        integer simulated
        text timestamp
    }

    TIMELINE_ENTRIES {
        text id PK
        text investigation_id FK
        text timestamp
        text entry_type
        text title
        text description
        text event_ids
        text evidence_ids
        text hypothesis_ids
        text decision_id
        text severity
    }
```

---

## 6. Intelligent Agent Architecture (تصميم الوكيل الذكي)

### 6.1 تأطير الوكيل وفق نموذج PEAS
- **Performance Measure (المقياس):** دقة حسم الفرضيات، تقليل خطوات التحقيق الزائدة، تجنب التصعيد الخاطئ (False Escalation)، وتتبع شفاف ومفسر 100% لكل قرار.
- **Environment (البيئة):** بيئة محاكاة رقمية (Simulated SOC Environment) تقرأ سجلات CSV/JSON ذات معلومات ناقصة أو غير كاملة.
- **Actuators (المُشغلات/الإجراءات):** إجراءات استقصائية آمنة (`REQUEST_ADDITIONAL_LOGS`, `ANALYZE_RELATED_EVENT`, `INVESTIGATE_ENTITY`, `REVIEW_EVIDENCE_RELATION`, `ESCALATE_FOR_HUMAN_REVIEW`, `CONCLUDE_INVESTIGATION`).
- **Sensors (المستشعرات):** محركات قراءة السجلات وتطبيعها وتغذية الأحداث الأمنية في مصفوفة الإدراك.

### 6.2 مخطط دورة اتخاذ القرار الوكيلاتي الكاملة

```mermaid
flowchart TD
    Start([بدء التحقيق أو استقبال بيانات جديدة]) --> Perception[1. الإدراك والتصفية Perception]
    Perception --> UpdateState[2. تحديث الكيانات والحالة الداخلية State Update]
    UpdateState --> EvalHypo[3. تقييم الفرضيات وكشف النقص والمنافاة]
    EvalHypo --> GenActions[4. توليد الإجراءات المرشحة Candidate Generation]
    GenActions --> CalcUtility[5. حساب المنفعة: U = Benefit - Cost - Risk]
    CalcUtility --> SelectBest[6. اختيار الإجراء الأعلى منفعة Action Selection]
    SelectBest --> GenExplanation[7. توليد التفسير المنطقي Explanation]
    GenExplanation --> CheckStop{هل تحقق شرط توقف؟}
    CheckStop -- نعم --> Conclude[إنهاء التحقيق وتثبيت النتيجة]
    CheckStop -- لا --> ExecAction[8. تنفيذ الإجراء في بيئة المحاكاة]
    ExecAction --> ReceiveFeedback[9. استقبال التغذية الراجعة Feedback]
    ReceiveFeedback --> UpdateState
```

---

## 7. Evidence Correlation Architecture (معمارية محرك ربط الأدلة)

### 7.1 مبدأ "الارتباط لا يعني السببية"
يقتصر محرك الارتباط على استكشاف العلاقات الإحصائية والسياقية بين الأحداث (Contextual Proximity)، ويسجل نوع العلاقة ووزنها دون إطلاق أحكام مسبقة؛ إذ يترك الاستنتاج والترجيح لمحرك الفرضيات والوكيل الذكي.

### 7.2 مصفوفة قواعد الارتباط (Correlation Rules Matrix)

| القاعدة | الشرط المنطقي | نوع الحافة الناتجة | الوزن $W$ | درجة الثقة $C$ |
| :--- | :--- | :--- | :---: | :---: |
| **SAME_ACCOUNT** | تطابق `account_id` بين حدثين خلال نافذة زمنية $\le 1\text{ hr}$ | `SAME_ACCOUNT` | 0.90 | 0.95 |
| **SAME_DEVICE** | تطابق `device_id` بين حدثين خلال نافذة زمنية $\le 1\text{ hr}$ | `SAME_DEVICE` | 0.85 | 0.90 |
| **TEMPORAL_WINDOW** | وقوع حدثين خلال نافذة قصيرة $\le 300\text{ sec}$ | `TEMPORALLY_RELATED` | $1 - \frac{\Delta t}{300}$ | دالة متناقصة |
| **NETWORK_RELATION** | تقاطع IP المصدر والهدف بين حدثين (اتصال متبادل) | `NETWORK_RELATED` | 0.80 | 0.85 |
| **SAME_INDICATOR** | تطابق عنوان IP خارجي مشبوه أو تجزئة ملف (Hash) | `SAME_INDICATOR` | 0.95 | 0.90 |

### 7.3 تمثيل رسم الأدلة باستخدام NetworkX
يُبنى الرسم كرسم بياني موجه متعدد الخصائص `nx.DiGraph`:
- **العقد (Nodes):** تمثل الأحداث الأمنية والأدلة مع سمات: `event_type`, `severity`, `timestamp`, `reliability`.
- **الحواف (Edges):** تمثل العلاقات المستخرجة مع سمات: `relation_type`, `weight`, `confidence`, `temporal_delta`.

```mermaid
graph LR
    E1["Event 1: Failed Login<br/>User: Alice | WS-001<br/>02:15:00"]
    E2["Event 2: Failed Login<br/>User: Alice | WS-001<br/>02:15:05"]
    E3["Event 3: Success Login<br/>User: Alice | WS-001<br/>02:15:40"]
    E4["Event 4: Outbound Connection<br/>From: WS-001 To: SRV-002<br/>02:16:10"]

    E1 -->|SAME_ACCOUNT & SAME_DEVICE<br/>Weight: 0.95| E2
    E2 -->|SAME_ACCOUNT & SAME_DEVICE<br/>Weight: 0.95| E3
    E3 -->|TEMPORAL & SAME_DEVICE<br/>Weight: 0.88| E4
```

---

## 8. Hypothesis & Timeline Architecture (إدارة الفرضيات والخط الزمني)

### 8.1 حساب مستوى الثقة بالفرضية (Confidence Scoring)
يتم تحديث ثقة كل فرضية بطريقة حتمية خاضعة للمعادلة التالية:
$$\text{Confidence}(H) = \text{Clamp}_{[0, 1]} \left( \frac{\sum_{e \in S} \text{Rel}(e)}{\max(|S|, 1)} - \lambda_c \sum_{e \in C} \text{Rel}(e) - \lambda_m |M| \right)$$

حيث:
- $S$: مجموعة الأدلة الداعمة (Supporting Evidence).
- $C$: مجموعة الأدلة المعارضة (Contradicting Evidence).
- $M$: قائمة أنواع الأدلة الناقصة (Missing Evidence Types).
- $\text{Rel}(e)$: موثوقية الدليل (Reliability بين 0.0 و 1.0).
- $\lambda_c = 0.5$: معامل العقوبة للأدلة المتعارضة.
- $\lambda_m = 0.05$: معامل خفض الثقة لكل معلومة جوهرية مفقودة.

### 8.2 شروط انتقال الحالات والحماية من التأكيد المبكر
- لا تنتقل الفرضية إلى `CONFIRMED` إلا إذا كانت الثقة $\ge 0.85$ **وكانت قائمة الأدلة المفقودة فارغة تماماً** ($M = \emptyset$). هذا يمنع التأكيد المتسرع (Premature Confirmation).
- إذا كانت الثقة $\ge 0.75$ مع وجود نقص في الأدلة، تنتقل الفرضية إلى `ESCALATED` لمراجعة المحلل البشري.
- إذا هبطت الثقة إلى $\le 0.20$، تُعتبر الفرضية `REJECTED`.

---

## 9. Service/API Contracts as Design Specifications (عقود الخدمات والواجهات البرمجية)

> **ملاحظة تصميمية:** هذه الواجهات هي **مواصفات تصويرية توجيهية** (Design Specifications) تُعرّف كيف ستتخاطب المكونات لاحقاً دون كتابتها كملفات حالياً.

### 9.1 عقد خدمة التحقيق الموجهة للواجهة (Application Layer Service Contract)

```python
class IInvestigationService(Protocol):
    """الواجهة البرمجية الموحدة المتاحة لواجهة Streamlit والاختبارات"""
    
    def start_new_investigation(self, name: str, log_file_paths: list[str]) -> str:
        """تهيئة تحقيق جديد، استيراد السجلات، وتوليد الحالة الأولية"""
        ...

    def execute_next_step(self, investigation_id: str) -> dict:
        """تشغيل دورة وكيل واحدة: استدلال -> اختيار إجراء -> تنفيذ محاكى -> تحديث الحالة"""
        ...

    def run_to_completion(self, investigation_id: str, max_steps: int = 20) -> dict:
        """تشغيل التحقيق المتتابع تلقائياً حتى استيفاء شروط التوقف"""
        ...

    def get_summary_metrics(self, investigation_id: str) -> dict:
        """إرجاع إحصائيات لوحة التحكم: الفرضيات، الأدلة، مستوى الخطورة"""
        ...

    def get_graph_visual_data(self, investigation_id: str) -> dict:
        """تجهيز العقد والحواف في صيغة JSON مهيأة لرسم Plotly Network Graph"""
        ...

    def get_timeline_records(self, investigation_id: str) -> list[dict]:
        """إرجاع الخط الزمني مرتباً كرونولوجياً لعرضه في الواجهة"""
        ...
```

### 9.2 عقد وحدة الاستيراد (Member 1 Contract)

```python
class IEventIngester(Protocol):
    def ingest_and_validate(self, file_path: str) -> tuple[list[SecurityEvent], list[dict]]:
        """قراءة السجلات، تنظيفها، وفرز الأحداث الصالحة عن التالفة/المكررة"""
        ...
```

### 9.3 عقد محرك الارتباط (Member 2 Contract)

```python
class ICorrelationEngine(Protocol):
    def correlate_events(self, events: list[SecurityEvent]) -> tuple[list[Evidence], list[EvidenceRelation]]:
        """بناء علاقات الارتباط والأدلة المستخلصة دون افتراض السببية"""
        ...

    def export_networkx_graph(self) -> Any:
        """إرجاع كائن NetworkX DiGraph لاستخدامه في التحليل الرياضي والتصور"""
        ...
```

### 9.4 عقد محرك الفرضيات (Member 4 Contract)

```python
class IHypothesisEngine(Protocol):
    def evaluate(self, current_evidence: list[Evidence]) -> list[Hypothesis]:
        """صياغة وتحديث الفرضيات وتحديد الأدلة الناقصة المطلوبة"""
        ...
```

### 9.5 عقد نواة الوكيل الذكي (Member 3 Contract)

```python
class IAgentCore(Protocol):
    def evaluate_and_decide(self, state: InvestigationState) -> AgentDecision:
        """حساب دالة المنفعة U(a) لكل إجراء مرشح واختيار الأعلى منفعة وتوليد التفسير"""
        ...

    def apply_feedback(self, state: InvestigationState, result: ActionResult) -> InvestigationState:
        """تحديث الحالة الداخلية للوكيل استجابة لنتائج تنفيذ الإجراء"""
        ...
```

---

## 10. SQLite Database Design (تفاصيل قاعدة البيانات والتخزين)

### 10.1 استراتيجية الفصل بين المخزن والمحسوب ديناميكياً
- **يُخزّن في SQLite:** السجلات الأصلية المنظفة، الأدلة المستخلصة، الفرضيات المعتمدة وسجل تطورها، سجل كل قرار للوكيل (`AgentDecision`) مع التفسير والمنفعة، وسجلات الخط الزمني.
- **يُحسب ديناميكياً في الذاكرة (Runtime In-Memory):** كائن `NetworkX DiGraph` (يُبنى عند الطلب لسرعة العمليات)، ومصفوفات المسافات الزمنية المؤقتة أثناء التحليل.

### 10.2 تفاصيل الجداول ومفاتيحها وفهارسها
1. **`investigations`:**
   - الحقول: `id` (TEXT PK), `name` (TEXT), `status` (TEXT), `created_at` (TEXT), `updated_at` (TEXT).
2. **`security_events`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `timestamp` (TEXT), `event_type` (TEXT), `severity` (TEXT), `account_id` (TEXT), `device_id` (TEXT), `source_ip` (TEXT), `destination_ip` (TEXT), `validation_status` (TEXT).
   - الفهارس: `idx_events_inv_time` على `(investigation_id, timestamp)`.
3. **`evidence`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `evidence_type` (TEXT), `source_event_id` (TEXT), `reliability` (REAL), `observed_value` (TEXT), `timestamp` (TEXT).
4. **`evidence_relations`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `source_evidence_id` (TEXT), `target_evidence_id` (TEXT), `relation_type` (TEXT), `weight` (REAL), `confidence` (REAL).
5. **`hypotheses`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `description` (TEXT), `status` (TEXT), `confidence` (REAL), `missing_evidence_types` (TEXT JSON), `history` (TEXT JSON).
6. **`agent_decisions`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `step` (INTEGER), `action_type` (TEXT), `utility_score` (REAL), `benefit` (REAL), `cost` (REAL), `risk` (REAL), `explanation` (TEXT), `timestamp` (TEXT).
   - الفهارس: `idx_decisions_inv` على `(investigation_id, step)`.
7. **`timeline_entries`:**
   - الحقول: `id` (TEXT PK), `investigation_id` (TEXT FK), `timestamp` (TEXT), `entry_type` (TEXT), `title` (TEXT), `description` (TEXT), `severity` (TEXT).

---

## 11. Proposed Repository Structure (هيكل المستودع المقترح)

تم تنظيم المستودع ليمنح كل مطور نطاقاً معزولاً للعمل، مع وجود مجلدات مركزية مشتركة:

```text
tracemind/
│
├── app/
│   ├── domain/                  # [ملك للجميع بإشراف M6] النماذج الموحدة والعقود الصارمة
│   │   ├── __init__.py
│   │   ├── models.py            # SecurityEvent, Evidence, Hypothesis, Decision
│   │   └── contracts.py         # Interfaces / Protocols
│   │
│   ├── application/             # [مسؤولية M6 بالتعاون مع M5] خدمات التطبيق
│   │   ├── __init__.py
│   │   ├── investigation_service.py
│   │   └── report_service.py
│   │
│   ├── infrastructure/          # [مسؤولية M1 + M6] قاعدة البيانات والإعدادات
│   │   ├── __init__.py
│   │   ├── database.py          # SQLite Manager & Connection
│   │   └── config.py            # أوزان الوكيل ومعايير النوافذ الزمنية
│   │
│   ├── ingestion/               # [مسؤولية Member 1] استيراد وتنظيف وتطبيع السجلات
│   │   ├── __init__.py
│   │   ├── csv_parser.py
│   │   ├── json_parser.py
│   │   ├── normalizer.py
│   │   └── deduplicator.py
│   │
│   ├── correlation/             # [مسؤولية Member 2] محرك الارتباط وشبكة NetworkX
│   │   ├── __init__.py
│   │   ├── rules.py             # قواعد SAME_ACCOUNT, SAME_DEVICE, etc.
│   │   ├── graph_builder.py     # NetworkX Evidence Graph
│   │   └── correlation_engine.py
│   │
│   ├── agent/                   # [مسؤولية Member 3] نواة الوكيل وحساب المنفعة
│   │   ├── __init__.py
│   │   ├── perception.py
│   │   ├── utility_calculator.py# حساب U(a) = B - C - R
│   │   ├── action_generator.py
│   │   ├── explainer.py         # التفسير والتعليل
│   │   └── agent_core.py        # حلقة اتخاذ القرار الكاملة
│   │
│   ├── investigation/           # [مسؤولية Member 4] الفرضيات والخط الزمني
│   │   ├── __init__.py
│   │   ├── hypothesis_engine.py # دورة حياة الفرضية وتحديث الثقة
│   │   └── timeline_builder.py  # بناء الخط الزمني التراكمي
│   │
│   ├── ui/                      # [مسؤولية Member 5] واجهات Streamlit و Plotly
│   │   ├── __init__.py
│   │   └── pages/
│   │       ├── dashboard.py
│   │       ├── investigations.py
│   │       ├── timeline_view.py
│   │       ├── graph_view.py
│   │       ├── hypotheses_view.py
│   │       └── decisions_view.py
│   │
│   └── reporting/               # [مسؤولية Member 5] توليد التقارير
│       ├── __init__.py
│       └── report_generator.py
│
├── data/                        # البيانات والسيناريوهات
│   ├── raw/                     # سجلات الإدخال التجريبية
│   ├── normalized/              # مخرجات التطبيع
│   └── scenarios/               # سيناريوهات الاختبار المرجعية (Ground Truth)
│
├── tests/                       # [مسؤولية Member 6 بالتعاون مع الجميع]
│   ├── conftest.py              # المشتركات ومولدات البيانات الوهمية (Fixtures)
│   ├── unit/                    # اختبارات الوحدات المعزولة
│   ├── integration/             # اختبارات التكامل الثنائية
│   └── e2e/                     # اختبارات السيناريوهات الشاملة
│
├── docs/                        # التوثيق الشامل ومخططات النظام
│
├── scripts/
│   └── generate_synthetic_data.py # سكربت توليد بيانات المحاكاة
│
├── requirements.txt             # التبعيات الرسمية
├── README.md                    # دليل الاستخدام والتطوير
└── streamlit_app.py             # نقطة الدخول الرئيسية للواجهة
```

---

## 12. Team-of-6 Responsibilities (نموذج توزيع مسؤوليات المطورين الستة)

| العضو | الدور الرئيسي | الملفات المملوكة | المدخلات المستهلكة | المخرجات المقدمة لبقية الفريق |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1** | **Data Ingestion & Normalization** | `app/ingestion/`, `data/raw/`, `scripts/` | ملفات CSV/JSON خام | كائنات `SecurityEvent` موحدة وصالحة |
| **Member 2** | **Evidence Correlation Engine** | `app/correlation/` | كائنات `SecurityEvent` من M1 | كائنات `Evidence`, `EvidenceRelation`, و `nx.DiGraph` |
| **Member 3** | **Intelligent Agent Core** | `app/agent/` | أدلة M2 وفرضيات M4 | كائنات `AgentDecision`, `CandidateAction`, ودورة الوكيل |
| **Member 4** | **Hypothesis & Timeline Engine** | `app/investigation/` | أدلة M2 وقرارات M3 | كائنات `Hypothesis` محدثة وسجل `TimelineEntry` |
| **Member 5** | **Dashboard & Reporting** | `app/ui/`, `app/reporting/`, `streamlit_app.py` | واجهات `InvestigationService` | لوحة تحكم تفاعلية وتقارير بصرية للمستخدم |
| **Member 6** | **Testing, Integration & Architecture Lead** | `tests/`, `app/domain/`, `app/infrastructure/` | مخرجات جميع الأعضاء | بنية الاختبارات، قاعدة البيانات، والتحقق التكاملي |

---

## 13. Dependency Graph (مخطط التبعيات والتوازي)

```mermaid
flowchart TD
    M6_Models["Member 6: النماذج والعقود الموحدة\n(Shared Domain Models & Protocols)"]
    
    subgraph ParallelPhase1 ["مرحلة التطوير المستقل (الأسبوع 1 و 2 عبر الـ Mocks)"]
        M1_Ingestion["Member 1: معالجة السجلات وتوليد البيانات"]
        M2_Correlation["Member 2: محرك الارتباط وقواعد NetworkX"]
        M4_Hypothesis["Member 4: إدارة الفرضيات والخط الزمني"]
        M3_Agent["Member 3: دالة المنفعة واستدلال الوكيل"]
        M5_UI["Member 5: واجهات Streamlit و Plotly (بيانات تجريبية)"]
    end

    subgraph IntegrationPhase ["مرحلة التكامل المتتابع (نهاية الأسبوع 2 و 3)"]
        Int_1["تكامل Ingestion مع Correlation (M1 -> M2)"]
        Int_2["تكامل Correlation مع Hypotheses (M2 -> M4)"]
        Int_3["تكامل Hypotheses مع Agent Core (M4 -> M3)"]
        Int_4["ربط الوكيل بخدمة التطبيق وقاعدة البيانات (M3 -> M6)"]
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
    M5_UI --> Int_5
```

---

## 14. Parallel Development Strategy (استراتيجية التطوير المتوازي عبر الـ Mocks)

لمنع حدوث سيناريو الاختناق الكلاسيكي: *(العضو 5 ينتظر 4، و4 ينتظر 2، و2 ينتظر 1)*، يعتمد التصميم استراتيجية **Mock-Driven Isolation**:
1. **عقود مسبقة ملزمة في اليوم الثاني:** الاتفاق التام على `models.py` يُمكّن الجميع من العمل فوراً.
2. **استخدام Fixtures متطابقة:** يوفر العضو 6 ملف `conftest.py` يحتوي على مولدات أحداث وهمية (`mock_events`, `mock_evidence`, `mock_hypotheses`).
3. **تطوير الواجهة (Member 5):** يقوم Member 5 ببناء شاشات Streamlit ورسوم Plotly بالاعتماد على خدمة وهمية `MockInvestigationService` تُرجع بيانات مسبقة الإعداد، مما يتيح إنجاز الواجهة بالتوازي مع تطوير الخوارزميات.
4. **تطوير الوكيل (Member 3):** يختبر Member 3 دالة المنفعة $U(a)$ على حالات وهمية دون الحاجة لانتظار اكتمال معالجة السجلات الحقيقية.

---

## 15. Testing Architecture (استراتيجية الاختبار الشاملة)

```mermaid
pie title هرم الاختبارات لمشروع TraceMind
    "Unit Tests (اختبارات الوحدات المعزولة)": 70
    "Integration Tests (اختبارات التكامل بين المكونات)": 20
    "End-to-End Scenarios (سيناريوهات التحقيق الشاملة)": 10
```

### 15.1 محاور الاختبارات
1. **Unit Tests (تغطية $\ge 80\%$):**
   - اختبار قواعد الارتباط الخمسة كلٌّ على حدة (تأكيد النتيجة الصحيحة عند تحقق الشرط وعدم إنتاج علاقة عند عدم تحققه).
   - اختبار دالة المنفعة الرياضية $U(a) = B(a) - C(a) - R(a)$ لجميع أنواع الإجراءات.
   - اختبار تحديث ثقة الفرضية وفق الأدلة الإيجابية والسلبية والناقصة.
2. **Integration Tests:**
   - تدفق الأحداث من Ingestion إلى Correlation والتأكد من بناء شبكة NetworkX بالشكل المطلوب.
   - تفاعل الوكيل مع محرك الفرضيات والتأكد من استجابة الوكيل للمعلومات المفقودة.
   - حفظ واسترجاع دورة التحقيق الكاملة من وإلى SQLite.
3. **End-to-End Scenarios:**
   - التحقق ضد 3 سيناريوهات مرجعية (`Ground Truth`):
     - **السيناريو 1 (Brute Force + Lateral Movement):** التأكد من وصول الوكيل لقرار طلب السجلات ثم التصعيد.
     - **السيناريو 2 (Normal IT Activity):** التأكد من عدم التصعيد وإغلاق التحقيق بنجاح (`CONCLUDE_INVESTIGATION`).
     - **السيناريو 3 (Contradictory Evidence):** التأكد من رفض الفرضية أو خفض ثقتها عند ظهور أدلة معارضة قاطعة.

---

## 16. Four-Week Implementation Roadmap (الخطة التنفيذية المفصلة لـ 4 أسابيع)

```mermaid
gantt
    title خطة التنفيذ لستة مطورين (TraceMind 4-Week Schedule)
    dateFormat  YYYY-MM-DD
    section Week 1 (البنية والعقود)
    إعداد المستودع ونماذج البيانات المشتركة (M6) :w1_1, 2026-11-01, 3d
    تجهيز السيناريوهات الاصطناعية و CSV/JSON (M1) :w1_2, 2026-11-01, 5d
    هيكل قواعد الارتباط و NetworkX (M2) :w1_3, 2026-11-03, 4d
    هيكل دورة حياة الفرضيات والخط الزمني (M4) :w1_4, 2026-11-03, 4d
    صياغة نموذج الحالة ودالة المنفعة للوكيل (M3) :w1_5, 2026-11-03, 4d
    هيكل واجهة Streamlit مع بيانات تجريبية (M5) :w1_6, 2026-11-04, 3d
    
    section Week 2 (المنطق الأساسي)
    تطوير Ingestion الكامل والتنظيف (M1) :w2_1, 2026-11-08, 5d
    تطوير قواعد محرك الارتباط وحساب الأوزان (M2) :w2_2, 2026-11-08, 5d
    تطوير محرك الفرضيات ومعادلة الثقة (M4) :w2_3, 2026-11-08, 5d
    تطوير استدلال الوكيل وتوليد الإجراءات U(a) (M3) :w2_4, 2026-11-08, 5d
    تطوير صفحات الخط الزمني واستكشاف الأدلة (M5) :w2_5, 2026-11-08, 5d
    بناء مخطط SQLite واختبارات التكامل الأولية (M6) :w2_6, 2026-11-08, 5d

    section Week 3 (التكامل وحلقة الوكيل)
    ربط الاستيراد مع الارتباط وتغذية الأدلة (M1+M2) :w3_1, 2026-11-15, 4d
    تشغيل حلقة الوكيل الكاملة واستقبال التغذية (M3+M4) :w3_2, 2026-11-15, 5d
    ربط واجهة Streamlit بالخدمات الحقيقية (M5) :w3_3, 2026-11-17, 4d
    تفعيل التخزين الدائم في SQLite لكافة الحركات (M6) :w3_4, 2026-11-15, 5d

    section Week 4 (الاختبارات الشاملة والعرض)
    تنفيذ اختبارات E2E على السيناريوهات المرجعية (M6) :w4_1, 2026-11-22, 4d
    تحسين الشرح والتعليل وإحكام شروط التوقف (M3) :w4_2, 2026-11-22, 3d
    تحسين مظهر الرسوم البيانية وتوليد التقارير (M5) :w4_3, 2026-11-22, 4d
    التوثيق النهائي، تقرير المشروع، وتحضير العرض التوضيحي (الجميع) :w4_4, 2026-11-25, 4d
```

---

## 17. MVP Scope (نطاق المنتج الأولي القابل للتطبيق)

- **Must Have (ضروري جداً لإثبات الوكيل):**
  - قراءة ملفات CSV و JSON ومعالجتها وتطبيعها.
  - تطبيق قواعد الارتباط الخمسة وبناء رسم NetworkX للأدلة.
  - إدارة الفرضيات وتحديث درجات الثقة استناداً للأدلة.
  - تشغيل دورة الوكيل الذكي: توليد الإجراءات، حساب $U(a) = B - C - R$، اختيار الإجراء، والمحاكاة.
  - شرح نصي شفاف للقرارات المتخذة.
  - واجهة Streamlit تعرض الخط الزمني، شبكة الأدلة (Plotly)، وحالة الفرضيات وقرارات الوكيل.
  - حفظ واسترجاع التحقيقات عبر SQLite محلياً.
- **Should Have (مهم):**
  - تصدير تقرير التحقيق النهائي بصيغة نصية أو ملخص قابل للتنزيل.
  - معالجة تعارض الأدلة وتراجع الثقة التلقائي.
- **Out of Scope (خارج النطاق المعتمد):**
  - الاتصال بأنظمة أمنية حقيقية أو واجهات API حية لأجهزة إنتاجية.
  - استخدام نماذج لغوية ضخمة مدفوعة (LLM APIs) أو خدمات سحابية.
  - تقنيات الحاويات المعقدة (Kubernetes / Docker) وأنظمة قواعد البيانات الموزعة.

---

## 18. First Vertical Slice (الشريحة الرأسية الأولى للتحقق السريع)

لضمان سلامة الهيكل المعماري في أقرب وقت، تُحدّد الشريحة الرأسية الأولى (Vertical Slice) ليتم إنجازها واختبارها في نهاية **الأسبوع الأول / بداية الأسبوع الثاني**:

```mermaid
flowchart LR
    CSV["ملف CSV مصغر (3 أحداث: 2 فشل + 1 نجاح)"] --> Ingest["استيراد وتطبيع"]
    Ingest --> Correlate["ربط SAME_ACCOUNT"]
    Correlate --> Hypo["توليد فرضية Brute Force بنسبة ثقة 0.65"]
    Hypo --> Agent["حساب المنفعة لاختيار طلب سجلات إضافية"]
    Agent --> Decision["اتخاذ قرار توليد التفسير"]
    Decision --> UI["عرض النتيجة في جدول Streamlit مبسط"]
```

**الهدف من هذه الشريحة:** إثبات أن تدفق البيانات يمر عبر طبقات المطورين الستة بدون أخطاء توافقية في الأنواع والواجهات.

---

## 19. Architecture Decisions and Risks (سجلات القرارات والمخاطر)

### 19.1 سجلات القرارات المعمارية الرئيسية (ADR Summaries)
- **ADR-001 (Modular Monolith):** تم اعتماد الكتلي المعياري لتقليل الهدر التشغيلي والتركيز الكامل على منطق الوكيل الذكي ومناسبته للجدول الزمني المكون من 4 أسابيع.
- **ADR-002 (Utility-Based Agent Formulation):** اعتماد صياغة المنفعة $U(a) = B(a) - C(a) - R(a)$ لضمان الحتمية الرياضية وقابلية التفسير وتجنب القرارات العشوائية للنماذج غير المضبوطة.
- **ADR-003 (NetworkX for Evidence Correlation):** اعتماد NetworkX كبنية بيانات مرنة لحساب المسارات والعلاقات وتحويلها بسهولة إلى رسوم بيانية تفاعلية عبر Plotly.
- **ADR-004 (SQLite Local Storage):** استخدام SQLite المدمج مع Python دون الحاجة لتنصيب خوادم قواعد بيانات إضافية لضمان سهولة تشغيل المشروع على أجهزة المشرفين والطلاب.

### 19.2 سجل المخاطر وخطة تخفيفها (Risk Management)

| المخاطرة | الاحتمالية | الأثر | استراتيجية التخفيف والوقاية |
| :--- | :---: | :---: | :--- |
| **تضارب أعضاء الفريق في نماذج البيانات** | متوسطة | عالي جداً | حظر تعديل `app/domain/models.py` إلا بعد موافقة رسمية من مسؤول التكامل (Member 6) ومراجعة جميع الأعضاء. |
| **تداخل منطق العمل داخل Streamlit** | عالية | عالي | فرض قيود معمارية صارمة: واجهة Streamlit تستدعي دوال `InvestigationService` فقط ولا تتضمن استعلامات SQL أو حسابات منفعة. |
| **تعطل المطورين بسبب تأخر المراحل السابقة** | متوسطة | عالي | إلزام كل عضو بتوفير واجهات وهمية (Stubs/Mocks) فور تسليم العقود المشتركة لبدء العمل المتوازي. |
| **التأكيد المتسرع للاختراق (Premature Confirmation)** | متوسطة | متوسط | اشتراط خلو قائمة الأدلة الناقصة ($M = \emptyset$) وتجاوز حد الثقة ($> 0.85$) قبل تأكيد الفرضية. |

---

# خلاصة

هذه الوثيقة تمثل **المواصفات المعمارية الكاملة والتفصيلية الجاهزة للتنفيذ** لمشروع **TraceMind**. تم ضبطها بدقة لتلبي كافة متطلبات مقترح المشروع لمقرر Intelligent Agents، وتوزع المهام على المطورين الستة بالتساوي مع استقلالية تامة أثناء التطوير.
