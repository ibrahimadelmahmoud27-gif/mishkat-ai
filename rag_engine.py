"""
Mishkat AI - Knowledge Retrieval & Trust Engine (rag_engine.py)
تحدي الذكاء الاصطناعي في خدمة المحتوى الإسلامي 2026م
المسار المفتوح: «نُعلّم الآلة.. لتخدم الرسالة»
"""

import re
from typing import List, Dict, Any

class IslamicRAGEngine:
    def __init__(self):
        # قاعدة المعرفة التجريبية المصنفة وفق أوعية التحدي المعتمدة
        # (المستودع الدعوي dawa.center، موسوعة الجمهرة، والدرر السنية dorar.net)
        self.knowledge_base = [
            {
                "id": "kb_01",
                "topic": "معاملة الجار والأخلاق",
                "keywords": ["جار", "جيران", "أخلاق", "معاملة", "إحسان"],
                "text": "ما زالَ جِبْرِيلُ يُوصِينِي بالجارِ، حتَّى ظَنَنْتُ أنَّه سَيُوَرِّثُهُ.",
                "source": "صحيح البخاري",
                "section": "كتاب الأدب - باب الوصاة بالجار",
                "reference": "حديث رقم 6014، الجزء 8، صفحة 10",
                "url": "https://dorar.net/hadith/sharh/1234",
                "authenticity": "صحيح (أعلى درجات الصحة)",
                "base_trust": 98.5
            },
            {
                "id": "kb_02",
                "topic": "الرحمة والتواصل الإنساني",
                "keywords": ["رحمة", "إنسانية", "عالمين", "تراحم", "أخلاق النبي"],
                "text": "وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ.",
                "source": "القرآن الكريم",
                "section": "سورة الأنبياء، الآية 107",
                "reference": "تفسير ابن كثير، المجلد 5، صفحة 385",
                "url": "https://quran.ksu.edu.sa/tafseer/katheer/sura21-aya107.html",
                "authenticity": "نص قرآني قطعي الثبوت والدلالة",
                "base_trust": 100.0
            },
            {
                "id": "kb_03",
                "topic": "التعريف بالإسلام وأركانه",
                "keywords": ["إسلام", "أركان", "تعريف بالإسلام", "شهادة", "صلاة"],
                "text": "بُنِيَ الإسْلامُ علَى خَمْسٍ: شَهادَةِ أنْ لا إلَهَ إلَّا اللَّهُ وأنَّ مُحَمَّدًا رَسولُ اللَّهِ، وإقامِ الصَّلاةِ، وإيتاءِ الزَّكاةِ، والحَجِّ، وصَوْمِ رَمَضانَ.",
                "source": "صحيح مسلم",
                "section": "كتاب الإيمان - باب بيان أركان الإسلام",
                "reference": "حديث رقم 16، الجزء 1، صفحة 45",
                "url": "https://dorar.net/hadith/sharh/5678",
                "authenticity": "صحيح متفق عليه",
                "base_trust": 99.0
            }
        ]

    def retrieve_context(self, user_query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        استرجاع السياق الموثق الأكثر ملاءمة للسؤال لمنع توليد إجابات دون إسناد
        """
        scores = []
        tokens = set(re.findall(r"\w+", user_query.lower()))

        for doc in self.knowledge_base:
            match_score = 0
            for kw in doc["keywords"]:
                if kw in user_query:
                    match_score += 2
            for token in tokens:
                if token in doc["text"]:
                    match_score += 1
            if match_score > 0:
                scores.append((match_score, doc))

        # ترتيب النتائج من الأعلى صلة
        scores.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scores[:top_k]]
        
        # في حال عدم وجود مطابقة مباشرة، نرجع المصدر العام الأقرب
        if not results and self.knowledge_base:
            results = [self.knowledge_base[0]]
            
        return results

    def calculate_trust_score(self, retrieved_docs: List[Dict[str, Any]]) -> float:
        """
        حساب مؤشر الثقة الرقمي (Trust Score %)
        بناءً على أصالة المصادر وتخريج الأدلة
        """
        if not retrieved_docs:
            return 70.0
        total = sum(doc.get("base_trust", 85.0) for doc in retrieved_docs)
        avg_score = round(total / len(retrieved_docs), 1)
        return min(avg_score, 100.0)

    def build_augmented_prompt(self, user_query: str, retrieved_docs: List[Dict[str, Any]], language: str = "ar") -> str:
        """
        دمج السياق الموثق داخل الأوامر الموجهة للنماذج اللغوية (Gemini / Groq)
        مع إلزامه بعدم الإجابة إلا من داخل هذا السياق
        """
        context_str = ""
        for i, doc in enumerate(retrieved_docs, 1):
            context_str += (
                f"\n[مرجع {i}]:\n"
                f"- النص: {doc['text']}\n"
                f"- المصدر: {doc['source']} ({doc['section']})\n"
                f"- التوثيق الدقيق: {doc['reference']}\n"
                f"- درجة الصحة: {doc['authenticity']}\n"
            )

        system_instruction = (
            "أنت مساعد منصة Mishkat AI (مشكاة) لخدمة المعرفة والتواصل الحضاري. "
            "أجب عن سؤال المستفيد بالاعتماد حصراً على المراجع الموثقة المرفقة أدناه. "
            "يجب أن تكون إجابتك رصينة، حضارية، وميسرة، مع ضرورة إسناد كل فكرة لمرجعها، "
            "والامتناع التام عن الفتوى الشخصية أو اختراع معلومات غير واردة في المراجع.\n"
        )

        prompt = (
            f"{system_instruction}\n"
            f"المراجع الشرعية المعتمدة المسترجعة:\n{context_str}\n\n"
            f"سؤال المستفيد: {user_query}\n\n"
            f"صِغ الإجابة الموثقة مع ذكر الهوامش والمراجع في نهايتها:"
        )
        return prompt

# ==========================================
# اختبار تشغيلي لمحرك الـ RAG
# ==========================================
if __name__ == "__main__":
    rag = IslamicRAGEngine()
    query = "كيف كان النبي صلى الله عليه وسلم يعامل جيرانه؟"
    
    docs = rag.retrieve_context(query)
    trust = rag.calculate_trust_score(docs)
    prompt = rag.build_augmented_prompt(query, docs)
    
    print(f"--- السؤال: {query} ---")
    print(f"عدد المصادر المسترجعة: {len(docs)}")
    print(f"مؤشر الثقة الرقمي (Trust Score): {trust}%")
    print(f"المصدر المسترجع: {docs[0]['source']} - {docs[0]['reference']}")
