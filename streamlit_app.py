import json
from pathlib import Path
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Merch Trend Hunter", page_icon="🎯", layout="wide")
DATA = Path("data/trends.json")
TEXT = {
"English": {"subtitle":"Daily US trend monitoring for POD research","market":"Market","status":"Build status","ready":"Daily collector configured","count":"Tracked trends","last":"Last collection","source":"Source","table":"US trending searches","empty":"No live collection saved yet. Run the workflow once from GitHub Actions.","warning":"Search interest is not product demand, sales, or proof a T-shirt will sell.","trend":"Trend","traffic":"Google traffic label","published":"Published","method":"How to interpret this feed","method_text":"This collector reads the Google Trends US trending-searches RSS feed. It records currently listed searches and the traffic label supplied by the feed. It does not provide historical growth, Amazon BSR, competitor counts, or verified sales.","next":"Next steps","next_text":"Add dated history and comparisons, then Amazon competition research using permitted sources.","language":"Language"},
"العربية": {"subtitle":"مراقبة يومية للترندات الأمريكية لأبحاث الطباعة عند الطلب","market":"السوق","status":"حالة البناء","ready":"تم إعداد جامع الترندات اليومي","count":"الترندات المرصودة","last":"آخر جمع","source":"المصدر","table":"عمليات البحث الرائجة في أمريكا","empty":"لم تُحفظ نتائج مباشرة بعد. شغّل سير العمل مرة واحدة من GitHub Actions.","warning":"الاهتمام بالبحث لا يعني طلباً على المنتجات أو مبيعات مؤكدة ولا يضمن بيع القميص.","trend":"الترند","traffic":"مؤشر الزيارات في Google","published":"تاريخ النشر","method":"كيفية فهم البيانات","method_text":"يقرأ هذا الجامع موجز Google Trends للترندات الأمريكية ويسجل عمليات البحث الظاهرة ومؤشر الزيارات الوارد في الموجز. لا يوفر نمواً تاريخياً أو BSR من Amazon أو عدد المنافسين أو مبيعات مؤكدة.","next":"الخطوات التالية","next_text":"إضافة سجل تاريخي ومقارنات، ثم أبحاث منافسة Amazon باستخدام مصادر وطرق وصول مسموح بها.","language":"اللغة"}}
with st.sidebar:
    st.title("🎯 Merch Trend Hunter")
    lang = st.radio("Language / اللغة", ["English","العربية"])
    st.divider()
    st.caption(TEXT[lang]["market"]); st.write("🇺🇸 United States")
    st.caption(TEXT[lang]["status"]); st.write("🟢 " + TEXT[lang]["ready"])
    st.caption("Version 0.2.0")
t = TEXT[lang]
try:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
except Exception:
    payload = {"items": [], "collected_at": None}
items = payload.get("items", [])
st.title("🎯 Merch Trend Hunter")
st.caption(t["subtitle"])
st.info(t["warning"], icon="ℹ️")
a,b,c = st.columns(3)
a.metric(t["count"], len(items)); b.metric(t["last"], payload.get("collected_at") or "—"); c.metric(t["source"], "Google Trends RSS")
st.subheader(t["table"])
if not items:
    st.warning(t["empty"])
else:
    df = pd.DataFrame(items)
    df = df.rename(columns={"title":t["trend"],"traffic_label":t["traffic"],"published":t["published"]})
    st.dataframe(df[[x for x in [t["trend"],t["traffic"],t["published"]] if x in df]], use_container_width=True, hide_index=True)
    for item in items:
        if item.get("news_url"):
            st.markdown(f'[{item.get("title","News")}]({item["news_url"]})')
l,r = st.columns(2)
with l:
    st.subheader(t["method"]); st.write(t["method_text"])
with r:
    st.subheader(t["next"]); st.write(t["next_text"])
st.caption("Collector timezone: UTC. Trend feed data is not sales data.")
