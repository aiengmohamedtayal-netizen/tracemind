# ADR-001: اختيار نمط Modular Monolith كمعمارية النظام

| الحقل | القيمة |
|-------|-------|
| **Title** | Architecture Pattern Selection: Modular Monolith |
| **Date** | 2026-10-26 |
| **Status** | ✅ Accepted |
| **Deciders** | فريق TraceMind (6 مطورين) |
| **Tags** | `architecture`, `monolith`, `modularity`, `design` |

---

## السياق (Context)

في بداية مشروع TraceMind، واجه الفريق قراراً معمارياً جوهرياً: أي نمط تصميمي يُحقق أفضل توازن بين **سرعة التطوير**، **وضوح الحدود**، و**قابلية الصيانة** في ضوء القيود الحقيقية للمشروع؟

### قيود المشروع الموثَّقة

| القيد | القيمة |
|-------|-------|
| **حجم الفريق** | 6 مطورين |
| **الجدول الزمني** | 4 أسابيع |
| **النطاق** | أكاديمي (Proof of Concept) |
| **اللغة** | Python (حصري) |
| **متطلبات النشر** | محلي (Local) — لا سحابة |
| **متطلبات التزامن** | مستخدم واحد في آن واحد |
| **متطلبات Scaling** | لا يوجد |

### المشكلة المحددة

كان الخيار الأولي **Pure Monolith** بسبب بساطته، لكن تجربة الفريق السابقة أثبتت أن غياب الحدود الواضحة بين الوحدات يؤدي إلى:
- تشابك الكود (Spaghetti Code) في المشاريع التي يعمل عليها أكثر من 3 مطورين
- صعوبة اختبار الوحدات بشكل منفصل (Unit Testing)
- خطر وضع Business Logic في طبقة UI دون رقيب معماري

في المقابل، **Microservices** كانت فكرة مطروحة بسبب شهرتها، لكن تكاليفها الهندسية تفوق قيمتها في السياق الحالي.

---

## القرار (Decision)

> **تم اختيار نمط Modular Monolith كمعمارية TraceMind.**

يُقسِّم هذا النمط التطبيق إلى **وحدات منطقية ذات حدود صريحة** داخل عملية نشر واحدة (Single Deployment Unit). كل وحدة تملك:
- مجلدها الخاص
- مسؤوليتها الواضحة
- واجهاتها (Interfaces) للتواصل مع الوحدات الأخرى

### الحدود الوحدوية المُعتمدة

```
app/
├── domain/          ← القلب — مشترك بين الجميع
├── ingestion/       ← وحدة الاستيعاب
├── correlation/     ← وحدة الارتباط
├── investigation/   ← وحدة التحقيق
├── agent/           ← وحدة الوكيل الذكي
├── reporting/       ← وحدة التقارير
├── ui/              ← وحدة العرض
└── infrastructure/  ← وحدة البنية التحتية
```

### قواعد التواصل بين الوحدات

```python
# ✅ مسموح: وحدة تستدعي وحدة أخرى عبر واجهتها
from app.domain.interfaces import AlertRepositoryInterface
from app.ingestion.service import IngestionService

# ❌ ممنوع: وحدة تستورد تطبيقاً محدداً من وحدة أخرى
from app.infrastructure.db.alert_repository import SQLiteAlertRepository  
# ↑ مسموح فقط في نقطة تجميع واحدة (Composition Root = main.py)
```

---

## النتائج (Consequences)

### ✅ النتائج الإيجابية

1. **وضوح التوزيع:** كل مطور من الستة يتملك وحدة منطقية واضحة، يقلل التعارضات (Merge Conflicts)
2. **قابلية الاختبار:** كل وحدة قابلة للاختبار بشكل مستقل عبر Dependency Injection
3. **سرعة التطوير:** لا يوجد إعداد Docker أو Service Discovery أو API Gateway
4. **مسار للتطوير المستقبلي:** إذا نما المشروع، يمكن نقل وحدة إلى Microservice بتكلفة أقل من إعادة الكتابة الكاملة
5. **دورة Debug بسيطة:** Stack trace واحد، process واحد، لا شبكة داخلية

### ⚠️ النتائج السلبية

1. **حدود تعاهدية فقط:** لا يوجد مُحوِّل (compiler) أو runtime يمنع خرق الحدود — يعتمد على انضباط الفريق وCode Review
2. **قاعدة بيانات مشتركة:** كل الوحدات تصل لـ SQLite نفسها عبر مستودعاتها — لا عزل حقيقي للبيانات
3. **نشر ذري (Atomic Deployment):** أي تغيير يتطلب نشر التطبيق كاملاً (مقبول في نطاقنا)
4. **قابلية التوسع:** لا يمكن scaling وحدة بعينها بشكل مستقل (غير مطلوب حالياً)

---

## البدائل المدروسة (Alternatives Considered)

### البديل الأول: Pure Monolith

**الوصف:** كود واحد متشابك، لا حدود واضحة بين المكونات.

```
tracemind/
├── main.py         ← كل شيء هنا
├── models.py
├── utils.py
└── app.py
```

**لماذا رُفض:**
- يُشجع على وضع Business Logic في أي مكان
- اختبار الوحدات شبه مستحيل بدون إعادة هيكلة
- مع 6 مطورين، يتحول إلى فوضى في الأسبوع الثاني

**الدرجة:** 3/10 (مناسب لمشروع فردي أو prototype سريع فقط)

---

### البديل الثاني: Microservices

**الوصف:** كل وحدة خدمة مستقلة بـ API خاص، تتواصل عبر HTTP/gRPC.

```
services/
├── ingestion-service/    (FastAPI + Docker)
├── correlation-service/  (FastAPI + Docker)
├── agent-service/        (FastAPI + Docker)
├── reporting-service/    (FastAPI + Docker)
└── ui-service/           (Streamlit + Docker)
# + API Gateway, Service Registry, Message Queue...
```

**التكاليف الإضافية المرفوضة:**
| التكلفة | التقدير |
|---------|---------|
| إعداد Docker Compose | يومان |
| تصميم REST APIs بين الخدمات | يومان |
| إدارة الحالة الموزعة | أسبوع |
| Distributed Tracing | يومان |
| **الإجمالي** | **~12 يوم** من أصل 28 |

**لماذا رُفض:**
- 43% من الجدول الزمني على بنية تحتية لا قيمة مضافة لها أكاديمياً
- تعقيد التصحيح (Debugging) يرتفع بشكل أسّي
- لا توجد متطلبات عمل (Business Requirements) تبرر هذا الاستثمار

**الدرجة:** 5/10 (ممتاز لفرق كبيرة ومنتجات إنتاجية — خاطئ هنا)

---

### البديل الثالث: Layered Monolith (بدون حدود وحدوية)

**الوصف:** تقسيم بالطبقات فقط (Presentation/Business/Data) بدون حدود وحدوية أفقية.

**لماذا رُفض:**
- يحل مشكلة الطبقات لكن لا يحل مشكلة التوزيع على 6 مطورين
- لا حدود واضحة لوحدة الارتباط أو التحقيق

---

## المراجع (References)

- Sam Newman, *Building Microservices*, O'Reilly (2019) — الفصل المتعلق بالـ Monolith
- Martin Fowler, *Patterns of Enterprise Application Architecture*
- [Modular Monolith: A Primer](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
- `docs/ARCHITECTURE.md` — التوثيق التفصيلي للمعمارية المختارة
