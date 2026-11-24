import streamlit as st
import pandas as pd
from datetime import datetime, timezone

st.set_page_config(
    page_title="Merch Trend Hunter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Starter build: sample rows are illustrative, not live market data.
SAMPLE = [
    {
        "topic": "Retro camping humor",
        "keyword": "funny camping vintage",
        "category": "Outdoors",
        "interest_growth": 42,
        "competition": 28,
        "freshness": 80,
        "merch_fit": 90,
        "risk": "Low",
        "source": "Demo data"
    },
    {
        "topic": "Teacher appreciation",
        "keyword": "teacher thank you gift",
        "category": "Education",
        "interest_growth": 31,
        "competition": 64,
        "freshness": 55,
        "merch_fit": 88,
        "risk": "Medium",
        "source": "Demo data"
    },
    {
        "topic": "Local wildlife tribute",
        "keyword": "wildlife memorial tribute",
        "category": "Animals",
        "interest_growth": 76,
        "competition": 35,
        "freshness": 92,
        "merch_fit": 83,
        "risk": "High review needed",
        "source": "Demo data"
    },
    {
        "topic": "Retro BBQ season",
        "keyword": "vintage bbq grill humor",
        "category": "Food & hobbies",
        "interest_growth": 25,
        "competition": 22,
        "freshness": 48,
        "merch_fit": 95,
        "risk": "Low",
        "source": "Demo data"
    },
]

TRANSLATIONS = {
    "English": {
        "subtitle": "US market research for print-on-demand designers",
        "dashboard": "Dashboard",
        "discovery": "Opportunity discovery",
        "settings": "Project settings",
        "market": "Market",
        "market_value": "United States",
        "status": "Build status",
        "status_value": "Starter version",
        "tracked": "Tracked topics",
        "avg_score": "Average opportunity score",
        "high": "High-potential topics",
        "table_title": "Opportunity watchlist",
        "demo": "DEMO DATA — illustrative examples only; not live Amazon results or verified sales.",
        "topic": "Topic",
        "keyword": "Keyword",
        "category": "Category",
        "growth": "Interest growth",
        "competition": "Competition",
        "freshness": "Freshness",
        "fit": "Merch fit",
        "risk": "Risk review",
        "score": "Opportunity score",
        "filter": "Filter by category",
        "all": "All",
        "method": "Scoring method",
        "method_text": "Starter formula: 30% interest growth + 25% low competition + 20% freshness + 25% Merch fit. Risk review is shown separately and will become a gate before publishing.",
        "next": "Next build steps",
        "next_text": "Connect approved trend sources, store dated observations, schedule automatic collection, then add Amazon competition research using permitted access methods.",
        "language": "Language",
        "last_updated": "Last updated",
    },
    "العربية": {
        "subtitle": "بحث السوق الأمريكي لمصممي الطباعة عند الطلب",
        "dashboard": "لوحة التحكم",
        "discovery": "اكتشاف الفرص",
        "settings": "إعدادات المشروع",
        "market": "السوق",
        "market_value": "الولايات المتحدة",
        "status": "حالة البناء",
        "status_value": "النسخة التأسيسية",
        "tracked": "المواضيع المتابعة",
        "avg_score": "متوسط تقييم الفرص",
        "high": "مواضيع واعدة",
        "table_title": "قائمة مراقبة الفرص",
        "demo": "بيانات تجريبية — أمثلة توضيحية فقط؛ ليست نتائج مباشرة من Amazon ولا مبيعات مؤكدة.",
        "topic": "الموضوع",
        "keyword": "الكلمة المفتاحية",
        "category": "الفئة",
        "growth": "نمو الاهتمام",
        "competition": "المنافسة",
        "freshness": "حداثة الترند",
        "fit": "ملاءمة Merch",
        "risk": "مراجعة المخاطر",
        "score": "درجة الفرصة",
        "filter": "تصفية حسب الفئة",
        "all": "الكل",
        "method": "طريقة التقييم",
        "method_text": "المعادلة الأولية: 30% نمو الاهتمام + 25% انخفاض المنافسة + 20% حداثة الترند + 25% ملاءمة Merch. تظهر مراجعة المخاطر بشكل منفصل وستصبح شرطاً قبل النشر.",
        "next": "خطوات البناء التالية",
        "next_text": "ربط مصادر الترندات المسموح بها، حفظ الملاحظات المؤرخة، جدولة الجمع التلقائي، ثم إضافة بحث منافسة Amazon باستخدام وسائل وصول مسموح بها.",
        "language": "اللغة",
        "last_updated": "آخر تحديث",
    }
}

def opportunity_score(row):
    low_competition = 100 - int(row["competition"])
    score = (
        0.30 * int(row["interest_growth"]) +
        0.25 * low_competition +
        0.20 * int(row["freshness"]) +
        0.25 * int(row["merch_fit"])
    )
    return round(score)

with st.sidebar:
    st.title("🎯 Merch Trend Hunter")
    lang = st.radio("Language / اللغة", ["English", "العربية"], horizontal=False)
    t = TRANSLATIONS[lang]
    st.divider()
    st.caption(t["market"])
    st.write("🇺🇸 " + t["market_value"])
    st.caption(t["status"])
    st.write("🧱 " + t["status_value"])
    st.divider()
    st.caption("Version 0.1.0")

t = TRANSLATIONS[lang]
st.title("🎯 Merch Trend Hunter")
st.caption(t["subtitle"])

df = pd.DataFrame(SAMPLE)
df["score"] = df.apply(opportunity_score, axis=1)
df = df.sort_values("score", ascending=False)

st.warning(t["demo"], icon="⚠️")

c1, c2, c3 = st.columns(3)
c1.metric(t["tracked"], len(df))
c2.metric(t["avg_score"], f'{df["score"].mean():.0f}/100')
c3.metric(t["high"], int((df["score"] >= 70).sum()))

st.subheader(t["table_title"])
categories = [t["all"]] + sorted(df["category"].unique().tolist())
chosen = st.selectbox(t["filter"], categories)
view = df if chosen == t["all"] else df[df["category"] == chosen]

display = view.rename(columns={
    "topic": t["topic"],
    "keyword": t["keyword"],
    "category": t["category"],
    "interest_growth": t["growth"],
    "competition": t["competition"],
    "freshness": t["freshness"],
    "merch_fit": t["fit"],
    "risk": t["risk"],
    "score": t["score"],
})
st.dataframe(
    display[[t["topic"], t["keyword"], t["category"], t["growth"],
             t["competition"], t["freshness"], t["fit"], t["risk"], t["score"]]],
    use_container_width=True,
    hide_index=True
)

left, right = st.columns(2)
with left:
    st.subheader(t["method"])
    st.write(t["method_text"])
with right:
    st.subheader(t["next"])
    st.write(t["next_text"])

st.caption(f'{t["last_updated"]}: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
