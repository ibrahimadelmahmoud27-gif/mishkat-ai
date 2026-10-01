"""
Mishkat AI - Knowledge Retrieval & Trust Engine (rag_engine.py)
تحدي الذكاء الاصطناعي في خدمة المحتوى الإسلامي 2026م
المسار المفتوح: «نُعلّم الآلة.. لتخدم الرسالة»
"""

import re
from typing import List, Dict, Any

class IslamicRAGEngine:
    def __init__(self):
        # قاعدة المعرفة المستندة حصراً إلى الأوعية المعتمدة للحزمة العلمية (ص 3-6)
        self.knowledge_base = [
            {
                "id": "kb_kaaba",
                "topic": "عبادة الله وحده وتوضيح مفهوم الكعبة",
                "keywords": ["الكعبة", "كعبة", "يعبد المسلمون", "عبادة الكعبة", "حجر", "تقديس", "worship kaaba"],
                "text": "المسلمون لا يعبدون الكعبة المشرفة قط، وإنما يعبدون الله وحده لا شريك له. الكعبة هي قبلة يتجه إليها المسلمون في صلاتهم لتوحيد وجهتهم بأمر الله، كما قال عمر بن الخطاب رضي الله عنه للحجر الأسود: 'إني أعلم أنك حجر لا تضر ولا تنفع، ولولا أني رأيت رسول الله ﷺ يقبلك ما قبلتك'.",
                "source": "المستودع الدعوي الرقمي (dawa.center) وصحيح البخاري",
                "section": "كتاب الحج - باب ما ذكر في الحجر الأسود",
                "reference": "حديث رقم 1597، الجزء 2، صفحة 151",
                "url": "https://dorar.net/hadith/sharh/14828",
                "authenticity": "صحيح متفق عليه",
                "base_trust": 99.5
            },
            {
                "id": "kb_quran_source",
                "topic": "مصدر القرآن الكريم ونفي تأليف البشر",
                "keywords": ["تأليف", "محمد", "القرآن من تأليف", "كتب القرآن", "مؤلف", "كلام الله", "authored"],
                "text": "القرآن الكريم هو كلام الله المعجز المنزل على نبيه محمد ﷺ باللفظ والمعنى عبر جبريل عليه السلام، وليس من تأليف البشر. وقد تحدى الله فصحاء العرب أن يأتوا بسورة من مثله فعجزوا، مع ثبوت أمية النبي ﷺ طوال حياته مصداقاً لقوله تعالى: {وَمَا كُنتَ تَتْلُوا۟ مِن قَبْلِهِۦ مِن كِتَـٰبٍۢ وَلَا تَخُطُّهُۥ بِيَمِينِكَ}.",
                "source": "مصحف مجمع الملك فهد وتفسير ابن كثير (المجلد 6، ص 182)",
                "section": "سورة العنكبوت، الآية 48 / سورة البقرة، الآية 23",
                "reference": "تفسير ابن كثير والدرر السنية في علوم القرآن",
                "url": "https://quranpedia.net/ar/verse/29-48",
                "authenticity": "نص قرآني قطعي الثبوت والدلالة",
                "base_trust": 100.0
            },
            {
                "id": "kb_sword",
                "topic": "حقيقة انتشار الإسلام ودفع شبهة السيف",
                "keywords": ["السيف", "بالسيف", "انتشر بالسيف", "إكراه", "حروب", "sword"],
                "text": "لم ينتشر الإسلام بالإكراه في الدين لقوله تعالى: {لَا إِكْرَاهَ فِي الدِّينِ}. والقتال شُرع للدفاع عن النفس ودفع العدوان وحماية حرية الدعوة، وأكبر بلدان العالم الإسلامي سكاناً اليوم (كإندونيسيا وماليزيا وغرب إفريقيا) دخلها الإسلام عبر المعاملة الحسنة للتجار دون أية معارك عسكرية.",
                "source": "المستودع الدعوي الرقمي - منصة بينات لدفع الشبهات",
                "section": "كتاب الجهاد - باب الوصاة بترك الغدر وقتل النساء والأطفال",
                "reference": "سنن أبي داود، حديث رقم 2614، الجزء 3، صفحة 37",
                "url": "https://dorar.net/hadith/sharh/21808",
                "authenticity": "صحيح / حسن",
                "base_trust": 98.7
            },
            {
                "id": "kb_differences",
                "topic": "أسباب اختلاف الفقهاء وسعة الشريعة",
                "keywords": ["مختلفة بين العلماء", "اختلاف العلماء", "أحكام مختلفة", "المذاهب", "الخلاف"],
                "text": "اختلاف العلماء المعتبر ليس تناقضاً في أصول الدين، بل هو سعة ورحمة وثراء تشريعي في الفروع والمسائل الظنية بحسب فهم الأدلة وتنوع مدارك الاستنباط، مع اتفاقهم الكامل والمطلق على أصول العقيدة وأركان الإسلام القطعية.",
                "source": "الدرر السنية - الموسوعة الفقهية (dorar.net/feqhia)",
                "section": "كتاب الاعتصام بالكتاب والسنة",
                "reference": "صحيح البخاري، حديث رقم 7352، الجزء 9، صفحة 108",
                "url": "https://dorar.net/hadith/sharh/23908",
                "authenticity": "صحيح البخاري",
                "base_trust": 99.0
            },
            {
                "id": "kb_fake_china",
                "topic": "التحقق من حديث اطلبوا العلم ولو بالصين وبيان بطلانه",
                "keywords": ["اطلبوا العلم", "الصين", "ولو في الصين", "ولو بالصين", "china"],
                "text": "تنبيه وتحقيق حديثي: عبارة 'اطلبوا العلم ولو في الصين' ليست حديثاً صحيحاً عن النبي ﷺ؛ بل حكم أئمة الحديث وجهابذة التخريج كابن حبان والعقيلي وابن الجوزي والألباني بأنه 'حديث باطل ومكذوب لا أصل له'، وتمنع القواعد العلمية نسبته للرسول ﷺ.",
                "source": "الدرر السنية - الموسوعة الحديثية (dorar.net/hadith)",
                "section": "كتب الموضوعات والأحاديث الضعيفة والباطلة",
                "reference": "الموضوعات لابن الجوزي، والمقاصد الحسنة للسخاوي ص 164",
                "url": "https://dorar.net/hadith/search?q=%D8%A7%D8%B7%D9%84%D8%A8%D9%88%D8%A7+%D8%A7%D9%84%D8%B9%D9%84%D9%85+%D9%88%D9%84%D9%88+%D9%81%D9%8A+%D8%A7%D9%84%D8%B5%D9%8A%D9%86",
                "authenticity": "باطل ومكذوب (لا أصل له)",
                "base_trust": 100.0
            },
            {
                "id": "kb_what_is_islam",
                "topic": "التعريف بالإسلام وأركانه الأساسية",
                "keywords": ["ما هو الاسلام", "what is islam", "الإسلام", "أركان الإسلام", "تعريف بالإسلام", "أركانه"],
                "text": "الإسلام هو الاستسلام لله بالتوحيد والانقياد له بالطاعة والبراءة من الشرك. يقوم على أركان خمسة أساسية: شهادة أن لا إله إلا الله وأن محمداً رسول الله، وإقام الصلاة، وإيتاء الزكاة، وصوم رمضان، وحج البيت لمن استطاع إليه سبيلاً.",
                "source": "صحيح مسلم - كتاب الإيمان",
                "section": "باب بيان أركان الإسلام ودعائمه العظام",
                "reference": "حديث رقم 16، الجزء 1، صفحة 45",
                "url": "https://dorar.net/hadith/sharh/24510",
                "authenticity": "صحيح متفق عليه",
                "base_trust": 99.8
            },
            {
                "id": "kb_neighbor",
                "topic": "حقوق الجار ومكارم الأخلاق الاجتماعية",
                "keywords": ["الجار", "جيران", "حق الجار", "الإحسان إلى الجار", "يعامل جيرانه", "neighbor"],
                "text": "يولي الإسلام حق الجار مكانة رفيعة وعظيمة في منظومة الأخلاق الاجتماعية؛ حيث حث القرآن والسنة على كف الأذى عنه والإحسان إليه ومواساته مسلماً كان أو غير مسلم، تأكيداً لقول النبي ﷺ: 'ما زال جبريل يوصيني بالجار حتى ظننت أنه سيورثه'.",
                "source": "صحيح البخاري - كتاب الأدب",
                "section": "باب الوصاة بالجار",
                "reference": "حديث رقم 6014، الجزء 8، صفحة 10",
                "url": "https://dorar.net/hadith/sharh/15923",
                "authenticity": "صحيح متفق عليه",
                "base_trust": 99.5
            },
            {
                "id": "kb_prophet_muhammad",
                "topic": "التعريف بالنبي محمد ﷺ وخاتم الرسالات",
                "keywords": ["who is prophet muhammad", "من هو محمد", "رسول الله", "نبي الإسلام", "prophet"],
                "text": "محمد ﷺ هو رسول الله وخاتم الأنبياء والمرسلين، أرسله الله رحمة للعالمين، ليدعو إلى عبادة الله الواحد ومكارم الأخلاق، مصدقاً لما بين يديه من رسالات الأنبياء كإبراهيم وموسى وعيسى عليهم السلام.",
                "source": "المستودع الدعوي وموسوعة الجمهرة",
                "section": "كتاب فضائل النبي ﷺ والأخلاق",
                "reference": "الأدب المفرد للبخاري، حديث رقم 273، صفحة 88",
                "url": "https://dorar.net/hadith/sharh/12975",
                "authenticity": "صحيح متفق عليه",
                "base_trust": 99.6
            }
        ]

    def retrieve_context(self, user_query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        query_clean = user_query.strip().lower()
        query_words = set(re.findall(r"\w+", query_clean))

        scored_docs = []
        for doc in self.knowledge_base:
            match_score = 0
            for kw in doc["keywords"]:
                if kw.lower() in query_clean:
                    match_score += 5
            for word in query_words:
                if len(word) > 2 and word in doc["text"].lower():
                    match_score += 1
            if match_score > 0:
                scored_docs.append((match_score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        if scored_docs:
            return [doc for _, doc in scored_docs[:top_k]]
        return []

    def calculate_trust_score(self, retrieved_docs: List[Dict[str, Any]]) -> float:
        if not retrieved_docs:
            return 85.0
        return retrieved_docs[0].get("base_trust", 98.5)

    def build_augmented_prompt(self, user_query: str, retrieved_docs: List[Dict[str, Any]], language: str = "ar") -> str:
        if not retrieved_docs:
            return "السؤال لا تتوافر له نصوص مباشرة ضمن أوعية الحزمة العلمية. امتنع بلطف وأحل للمختصين."

        doc = retrieved_docs[0]
        is_english = bool(re.search(r"[a-zA-Z]", user_query)) or (language == "en")

        if is_english:
            return (
                f"You are Mishkat AI assistant. Answer strictly using this verified Islamic reference:\n"
                f"Context: {doc['text']}\n"
                f"Source: {doc['source']} ({doc['reference']})\n"
                f"Question: {user_query}\n"
                f"Provide a clear, respectful answer in English, ending with the exact source citation."
            )
        else:
            return (
                f"أنت المساعد المعرفي لمنصة مشكاة (Mishkat AI). أجب بالاعتماد الحصري والمقيد على المرجع الموثق أدناه دون اختراع أو استطراد خارج السياق:\n\n"
                f"[المرجع المعتمد]:\n"
                f"- الموضوع: {doc['topic']}\n"
                f"- النص الشرعي: {doc['text']}\n"
                f"- المصدر: {doc['source']}\n"
                f"- التوثيق: {doc['section']} | {doc['reference']}\n"
                f"- درجة الصحة: {doc['authenticity']}\n\n"
                f"سؤال المستفيد: {user_query}\n\n"
                f"صِغ إجابة علمية واضحة ومباشرة مستندة حصراً إلى المرجع المذكور، واذكر المرجع بدقة في نهاية جوابك."
            )
