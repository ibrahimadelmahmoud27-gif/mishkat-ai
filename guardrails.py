import re

class IslamicGuardrails:
    def __init__(self):
        # 1. قائمة الكلمات الدلالية لطلبات الفتوى والنوازل (لحظر الإفتاء المستقل)
        self.fatwa_keywords = [
            r"\bما حكم\b", r"\bهل يجوز\b", r"\bهل يصح\b", r"\bهل حرام\b", r"\bهل حلال\b",
            r"\bأفتوني\b", r"\bأريد فتوى\b", r"\bما رأي الشرع\b", r"\bما حكم الشرع\b",
            r"\bطلاق\b", r"\bميراث\b", r"\bبيتكوين\b", r"\bفوركس\b", r"\bزكاة الشركات\b"
        ]
        
        # 2. قائمة دلالية للأسئلة العقائدية القطعية (لضمان توجيهها للمصادر الصارمة)
        self.aqeedah_keywords = [
            r"\bعذاب القبر\b", r"\bيوم القيامة\b", r"\bصفات الله\b", r"\bالملائكة\b", r"\bالقدر\b"
        ]

    def _check_patterns(self, text, patterns):
        """فحص النص مقابل قائمة من الأنماط النصية"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def validate_query(self, user_query: str) -> dict:
        """
        الوظيفة الأساسية: فحص السؤال وتصنيفه قبل السماح بمروره لمحرك RAG.
        ترجع قاموساً يحتوي على حالة القبول، التصنيف، ورسالة الإحالة إن وجدت.
        """
        # تنظيف مبدئي للنص
        clean_query = user_query.strip()

        # الفحص الأول: هل السؤال هو طلب فتوى أو نازلة فقهية معاصرة؟
        if self._check_patterns(clean_query, self.fatwa_keywords):
            return {
                "is_safe": False,
                "category": "Fatwa/Nawazel",
                "action": "Block_and_Refer",
                "message": (
                    "عفواً، أنا نظام 'مشكاة' للذكاء الاصطناعي مخصص للتعريف بالإسلام وتقديم المعلومات الموثقة. "
                    "أسئلتكم الفقهية وطلبات الفتوى تحتاج إلى تفصيل شرعي من جهات الاختصاص. "
                    "يُرجى التوجه لدار الإفتاء المعتمدة في بلدكم لضمان الدقة والأمانة العلمية."
                )
            }

        # الفحص الثاني: تصنيف الأسئلة العقائدية للتعامل معها بصرامة نصية
        if self._check_patterns(clean_query, self.aqeedah_keywords):
            return {
                "is_safe": True,
                "category": "Aqeedah_Qati",
                "action": "Strict_RAG",
                "message": "سؤال عقائدي قطعي، يوجه لمحرك البحث للالتزام الصارم بالنص."
            }

        # الفحص الثالث: الأسئلة العامة والدعوية (المسار الطبيعي)
        return {
            "is_safe": True,
            "category": "General_Dawah",
            "action": "Proceed",
            "message": "سؤال آمن ومعرفي، مسموح بالمرور للمحركات."
        }

# ==========================================
# تجربة الكود (للاختبار المحلي فقط)
# ==========================================
if __name__ == "__main__":
    guard = IslamicGuardrails()
    
    # تجربة 1: سؤال فتوى صريح
    test_1 = guard.validate_query("هل يجوز الاستثمار في الفوركس؟")
    print(f"تجربة 1 (الفتوى): {test_1['is_safe']} -> {test_1['message']}\n")
    
    # تجربة 2: سؤال تعريفي آمن
    test_2 = guard.validate_query("كيف كان النبي محمد يعامل جيرانه؟")
    print(f"تجربة 2 (دعوي): {test_2['is_safe']} -> {test_2['category']}\n")
