"""
Mishkat AI - LLM Router & Fallback Mechanism (llm_router.py)
منصة مشكاة للذكاء الاصطناعي - تحدي المحتوى الإسلامي 2026م
المسار المفتوح: «نُعلّم الآلة.. لتخدم الرسالة»
"""

import os
from google import genai
from groq import Groq

class LLMRouter:
    def __init__(self, gemini_key: str = None, groq_key: str = None):
        # قراءة المفاتيح بأمان من متغيرات البيئة السحابية (Streamlit Secrets)، مع خيار التمرير المباشر
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY", "")
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY", "")

        # تهيئة عميل Google Gemini إذا وُجد المفتاح
        self.gemini_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None
        
        # تهيئة عميل Groq إذا وُجد المفتاح
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None

    def _call_gemini(self, prompt: str) -> str:
        """المحرك الأساسي: Google Gemini 3.8 Flash"""
        if not self.gemini_client:
            raise ValueError("مفتاح Gemini API غير معرف في متغيرات البيئة.")
        response = self.gemini_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text

    def _call_groq(self, prompt: str) -> str:
        """المحرك البديل الفوري: Groq Llama 3.3 70B Versatile"""
        if not self.groq_client:
            raise ValueError("مفتاح Groq API غير معرف في متغيرات البيئة.")
        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت مساعد منصة Mishkat AI (مشكاة) المعرفي الموثوق."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # ضبط الحرارة لمنع الهلوسة والالتزام الصارم بالسياق
        )
        return completion.choices[0].message.content

    def generate_response(self, prompt: str) -> dict:
        """
        دالة التوجيه والتبديل التلقائي (Fallback Mechanism):
        تحاول أولاً مع Gemini، وإذا حدث أي عطل سحابي أو ضغط،
        تنتقل فوراً إلى Groq لضمان بقاء النظام متاحاً بنسبة 100%.
        """
        # المحاولة الأولى: المحرك الأساسي
        try:
            output_text = self._call_gemini(prompt)
            return {
                "success": True,
                "engine_used": "Gemini 3.8 Flash (الأساسي)",
                "response": output_text,
                "fallback_triggered": False
            }
        except Exception as gemini_error:
            # رصد الخطأ وبدء التحويل التلقائي للبديل الفوري
            print(f"⚠️ تنبيه تشغيلي: تعذر الاتصال بـ Gemini ({gemini_error}). جاري التبديل إلى Groq...")
            
            # المحاولة الثانية: المحرك الاحتياطي
            try:
                output_text = self._call_groq(prompt)
                return {
                    "success": True,
                    "engine_used": "Groq Llama 3.3 (البديل الفوري)",
                    "response": output_text,
                    "fallback_triggered": True,
                    "primary_error": str(gemini_error)
                }
            except Exception as groq_error:
                return {
                    "success": False,
                    "engine_used": None,
                    "response": "عفواً، تعذر الوصول إلى محركات الاستدلال في الوقت الحالي. يُرجى المحاولة لاحقاً.",
                    "error": f"Gemini Error: {gemini_error} | Groq Error: {groq_error}"
                }

# ==========================================
# اختبار تشغيلي للراوتر والتبديل
# ==========================================
if __name__ == "__main__":
    router = LLMRouter()
    test_prompt = "عرّف بمشروع مشكاة (Mishkat AI) في جملة واحدة موثقة."
    
    result = router.generate_response(test_prompt)
    print(f"الحالة: {result['success']}")
    print(f"المحرك المنفذ: {result['engine_used']}")
    print(f"هل تم تفعيل البديل؟: {result['fallback_triggered']}")
    print(f"نص الإجابة:\n{result['response']}")
