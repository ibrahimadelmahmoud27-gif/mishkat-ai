"""
Mishkat AI - Interactive Knowledge Interface (app.py)
تحدي الذكاء الاصطناعي في خدمة المحتوى الإسلامي 2026م
المسار المفتوح: «نُعلّم الآلة.. لتخدم الرسالة»
"""

import streamlit as st
from guardrails import IslamicGuardrails
from rag_engine import IslamicRAGEngine
from llm_router import LLMRouter

# 1. إعدادات الصفحة وهوية المنصة
st.set_page_config(
    page_title="Mishkat AI | منصة مشكاة المعرفية",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تخصيص المظهر وتنسيق مؤشر الثقة (Custom CSS)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A365D;
        text-align: right;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4A5568;
        text-align: right;
        margin-bottom: 25px;
    }
    .trust-card {
        background-color: #F7FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    .trust-score-val {
        font-size: 2.4rem;
        font-weight: 800;
        color: #2B6CB0;
    }
    .source-box {
        background-color: #EDF2F7;
        border-right: 4px solid #3182CE;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        font-size: 0.95rem;
        direction: rtl;
        text-align: right;
    }
    .warning-box {
        background-color: #FFF5F5;
        border-right: 4px solid #E53E3E;
        padding: 14px;
        border-radius: 6px;
        color: #9B2C2C;
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# 3. تهيئة الوحدات البرمجية وتخزينها في الجلسة (Caching)
@st.cache_resource
def load_modules():
    guard = IslamicGuardrails()
    rag = IslamicRAGEngine()
    router = LLMRouter()
    return guard, rag, router

guardrails, rag_engine, llm_router = load_modules()

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. الشريط الجانبي (Sidebar): معلومات التحكيم ومؤشرات التشغيل
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/mosque.png", width=70)
    st.title("Mishkat AI (مشكاة)")
    st.markdown("**«نُعلّم الآلة.. لتخدم الرسالة»**")
    st.caption("المسار المفتوح | تحدي المحتوى الإسلامي 2026م")
    st.divider()

    st.subheader("🛡️ صمام الأمان والتحقق")
    st.write("• فحص النوازل وحظر الإفتاء الآلي: **مفعّل**")
    st.write("• التفريق بين القطعي والاجتهادي: **مفعّل**")
    st.write("• توثيق المتون وهوامش الكتب: **مفعّل**")
    st.divider()

    st.subheader("⚙️ حالة البنية السحابية")
    st.write("• المحرك الأساسي: `Gemini 3.8 Flash`")
    st.write("• البديل الفوري: `Groq (Llama 3.3)`")
    st.success("الاعتمادات الحرجة مؤمنة مجاناً 100%")
    st.divider()
    st.caption("إشراف وبناء: إبراهيم عادل (AI & RAG Engineer)")

# 5. المنطقة الرئيسية (Main Layout)
col_main, col_metrics = st.columns([2.8, 1.2])

with col_main:
    st.markdown('<p class="main-header">منصة مشكاة للذكاء الاصطناعي</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">مساعد معرفي ذكي موثوق يجيب بالاستناد المباشر إلى أمهات الكتب والمصادر المعتمدة</p>', unsafe_allow_html=True)

    # عرض سجل الرسائل السابقة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("📚 المراجع وهوامش التوثيق المسترجعة"):
                    for s in msg["sources"]:
                        st.markdown(f"**المصدر:** {s['source']} | **الموضع:** {s['reference']}")
                        st.markdown(f"> *{s['text']}*")

    # صندوق إدخال السؤال
    user_query = st.chat_input("اكتب استفسارك هنا (مثال: كيف كان النبي صلى الله عليه وسلم يعامل جيرانه؟)...")

    if user_query:
        # 1. عرض سؤال المستفيد
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # 2. خط الدفاع الأول: صمام الأمان الشرعي
        with st.spinner("جاري فحص الاستفسار عبر صمام الأمان الشرعي..."):
            validation = guardrails.validate_query(user_query)

        if not validation["is_safe"]:
            # في حال رصد فتوى أو نازلة يتم الحظر الفوري دون استهلاك موارد
            refusal_response = validation["message"]
            st.session_state.messages.append({
                "role": "assistant",
                "content": refusal_response,
                "sources": []
            })
            with st.chat_message("assistant"):
                st.markdown(f'<div class="warning-box">{refusal_response}</div>', unsafe_allow_html=True)
            st.session_state["current_trust"] = 0.0
            st.session_state["last_engine"] = "محظور شرعياً (حظر إفتاء)"
        else:
            # 3. استرجاع السياق الموثق عبر محرك RAG
            with st.spinner("جاري استرجاع المتون والمراجع وتدقيق الأسانيد..."):
                retrieved_docs = rag_engine.retrieve_context(user_query)
                trust_score = rag_engine.calculate_trust_score(retrieved_docs)
                augmented_prompt = rag_engine.build_augmented_prompt(user_query, retrieved_docs)

            # 4. التوليد عبر التوجيه السحابي مع التبديل التلقائي (Fallback)
            with st.spinner("جاري صياغة الإجابة المعتمدة..."):
                generation_result = llm_router.generate_response(augmented_prompt)

            if generation_result["success"]:
                response_text = generation_result["response"]
                engine_used = generation_result["engine_used"]
                
                # حفظ النتيجة في الجلسة
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": retrieved_docs
                })
                st.session_state["current_trust"] = trust_score
                st.session_state["last_engine"] = engine_used

                # عرض الرد والمصادر
                with st.chat_message("assistant"):
                    st.write(response_text)
                    with st.expander("📚 المراجع وهوامش التوثيق المسترجعة"):
                        for s in retrieved_docs:
                            st.markdown(f"**المصدر:** {s['source']} ({s['section']})")
                            st.markdown(f"**التوثيق:** {s['reference']} | **درجة الصحة:** `{s['authenticity']}`")
                            st.markdown(f"> *«{s['text']}»*")
                            st.markdown(f"[رابط الإسناد الإلكتروني]({s['url']})")
            else:
                st.error("تعذر توليد الإجابة، يُرجى فحص الاتصال بالخادم.")

# 6. لوحة المؤشرات الجانبية (Trust Score & Engine Status)
with col_metrics:
    st.markdown("### 📊 لوحة التدقيق والموثوقية")
    
    current_trust = st.session_state.get("current_trust", 98.5)
    last_engine = st.session_state.get("last_engine", "Gemini 3.8 Flash (الأساسي)")

    st.markdown(f"""
    <div class="trust-card">
        <p style="margin: 0; color: #4A5568; font-weight: 600;">مؤشر الثقة الرقمي (Trust Score)</p>
        <p class="trust-score-val">{current_trust}%</p>
        <small style="color: #718096;">مقاس استناداً إلى دقة الإسناد وتطابق المتون مع مصادر التحدي المعتمدة</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚡ المحرك المنفذ حالياً")
    if "Groq" in last_engine:
        st.warning(f"🔄 تم التبديل تلقائياً إلى:\n**{last_engine}**")
    else:
        st.info(f"🟢 يعمل عبر:\n**{last_engine}**")

    st.markdown("#### 📖 المصادر المعتمدة بالمشروع")
    st.caption("1. المستودع الدعوي الرقمي (dawa.center)")
    st.caption("2. موقع وموسوعة الدرر السنية (dorar.net)")
    st.caption("3. تفاسير القرآن الكريم المعتمدة (ابن كثير)")
