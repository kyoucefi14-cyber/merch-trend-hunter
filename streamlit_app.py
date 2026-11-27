
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from keyword_collector import DEFAULT_SEEDS, collect_keywords
from keyword_engine import calculate_opportunity_score
from competition import (
    calculate_competition_score,
    get_competition_level,
    build_amazon_shirt_url,
)
from trademark_filter import check_trademark
from export_csv import export_to_csv


st.set_page_config(
    page_title="Merch Trend Hunter",
    page_icon="🎯",
    layout="wide",
)

DATA = Path("data/trends.json")

TEXT = {
    "English": {
        "subtitle": "US market research for print-on-demand designers",
        "market": "Market",
        "language": "Language",
        "trends": "Google Trends monitoring",
        "keywords": "Amazon keyword research",
        "collect": "Collect Amazon keywords",
        "seeds": "Seed keywords (separate with commas or new lines)",
        "limit": "Suggestions per seed",
        "count": "Collected keywords",
        "empty": "No keywords collected yet.",
        "trademark": "Trademark warning",
        "competition": "Competition analysis",
        "score": "Opportunity score",
        "demand": "Demand estimate",
        "trend": "Trend estimate",
        "intent": "Buyer intent estimate",
        "design": "Design potential estimate",
        "result_count": "Approximate result count",
        "exact_count": "Approximate exact-match count",
        "reviews": "Average reviews observed",
        "calculate": "Calculate opportunity score",
        "download": "Download CSV",
        "warning": "Autocomplete suggestions are not search volume or sales data.",
        "score_warning": "Scores based on manual estimates are research aids, not verified market measurements.",
        "trademark_warning": "No match does not mean legally safe. This is not legal clearance.",
        "competition_warning": "Competition indicators must be entered from your own observations. Result counts are approximate.",
        "saved": "Keywords collected successfully.",
        "no_competition": "Enter at least one competition indicator to calculate a score.",
        "select_keyword": "Select a keyword to evaluate",
        "amazon": "Amazon USA search",
        "niche": "Niche",
        "status": "Trademark status",
        "opportunity": "Opportunity",
        "method": "About this tool",
        "method_text": "Google Trends shows trending searches. Amazon Autocomplete provides keyword suggestions. Neither source proves product sales.",
        "last": "Last collection",
        "source": "Source",
        "tracked": "Tracked trends",
        "published": "Published",
        "traffic": "Google traffic label",
        "no_trends": "No trend data saved yet. Run the GitHub Actions workflow.",
    },
    "العربية": {
        "subtitle": "أبحاث السوق الأمريكي لمصممي الطباعة عند الطلب",
        "market": "السوق",
        "language": "اللغة",
        "trends": "مراقبة Google Trends",
        "keywords": "البحث عن كلمات Amazon",
        "collect": "اجمع كلمات Amazon",
        "seeds": "الكلمات الأساسية (افصل بينها بفواصل أو أسطر)",
        "limit": "عدد الاقتراحات لكل كلمة أساسية",
        "count": "عدد الكلمات المجموعة",
        "empty": "لم تجمع أي كلمات بعد.",
        "trademark": "تنبيه العلامات التجارية",
        "competition": "تحليل المنافسة",
        "score": "نقاط فرصة البيع",
        "demand": "تقدير الطلب",
        "trend": "تقدير الترند",
        "intent": "تقدير نية الشراء",
        "design": "تقدير قابلية التصميم",
        "result_count": "عدد نتائج البحث التقريبي",
        "exact_count": "عدد النتائج المطابقة التقريبي",
        "reviews": "متوسط مراجعات المنتجات التي شاهدتها",
        "calculate": "احسب نقاط الفرصة",
        "download": "تحميل ملف CSV",
        "warning": "اقتراحات البحث لا تمثل حجم البحث أو المبيعات الفعلية.",
        "score_warning": "النقاط المبنية على تقديرات يدوية هي أداة مساعدة وليست قياسات سوق مؤكدة.",
        "trademark_warning": "عدم وجود تطابق لا يعني أن الاستخدام آمن قانونيًا. هذا ليس فحصًا قانونيًا.",
        "competition_warning": "أدخل مؤشرات المنافسة التي رصدتها بنفسك. أعداد النتائج تقريبية.",
        "saved": "تم جمع الكلمات بنجاح.",
        "no_competition": "أدخل مؤشر منافسة واحدًا على الأقل لحساب النقاط.",
        "select_keyword": "اختر كلمة لتحليلها",
        "amazon": "بحث Amazon USA",
        "niche": "المجال",
        "status": "حالة العلامة التجارية",
        "opportunity": "الفرصة",
        "method": "حول الأداة",
        "method_text": "يعرض Google Trends عمليات البحث الرائجة، ويقدم Amazon Autocomplete اقتراحات كلمات. لا يثبت أي منهما مبيعات المنتجات.",
        "last": "آخر جمع",
        "source": "المصدر",
        "tracked": "الترندات المرصودة",
        "published": "تاريخ النشر",
        "traffic": "مؤشر زيارات Google",
        "no_trends": "لا توجد بيانات ترند محفوظة بعد. شغّل سير العمل من GitHub Actions.",
    },
}


with st.sidebar:
    st.title("🎯 Merch Trend Hunter")
    lang = st.radio("Language / اللغة", ["English", "العربية"])
    st.divider()
    st.write("🇺🇸 United States")
    st.caption("Version 0.3.0")

t = TEXT[lang]

st.title("🎯 Merch Trend Hunter")
st.caption(t["subtitle"])
st.info(t["warning"], icon="ℹ️")


# --------------------------------------------------
# Google Trends section - preserved from version 0.2
# --------------------------------------------------

st.header(t["trends"])

try:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
except Exception:
    payload = {"items": [], "collected_at": None}

trend_items = payload.get("items", [])

a, b, c = st.columns(3)
a.metric(t["tracked"], len(trend_items))
b.metric(t["last"], payload.get("collected_at") or "—")
c.metric(t["source"], "Google Trends RSS")

if trend_items:
    trend_df = pd.DataFrame(trend_items)

    rename_columns = {
        "title": "Trend",
        "traffic_label": t["traffic"],
        "published": t["published"],
    }

    trend_df = trend_df.rename(columns=rename_columns)

    visible_columns = [
        col for col in [
            "Trend",
            t["traffic"],
            t["published"],
        ]
        if col in trend_df.columns
    ]

    st.dataframe(
        trend_df[visible_columns],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning(t["no_trends"])


st.divider()


# --------------------------------------------------
# Amazon keyword research
# --------------------------------------------------

st.header(t["keywords"])

st.caption(t["warning"])

seed_text = st.text_area(
    t["seeds"],
    value=", ".join(DEFAULT_SEEDS),
    height=110,
)

limit_per_seed = st.slider(
    t["limit"],
    min_value=3,
    max_value=10,
    value=5,
)

if st.button(t["collect"], type="primary"):
    seeds = [
        item.strip()
        for item in seed_text.replace("\n", ",").split(",")
        if item.strip()
    ]

    if not seeds:
        st.error("Please enter at least one keyword.")
    elif len(seeds) > 30:
        st.error("Use no more than 30 seed keywords per collection.")
    else:
        try:
            with st.spinner("Collecting keyword suggestions..."):
                results = collect_keywords(
                    seed_keywords=seeds,
                    limit_per_seed=limit_per_seed,
                    delay_seconds=1.0,
                )

                for item in results:
                    keyword = item["keyword"]

                    trademark = check_trademark(keyword)

                    item.update({
                        "trademark_status": trademark[
                            "trademark_status"
                        ],
                        "matched_terms": trademark[
                            "matched_terms"
                        ],
                        "amazon_url": build_amazon_shirt_url(
                            keyword
                        ),
                        "competition_score": None,
                        "competition_level": "Unknown",
                        "demand_score": None,
                        "trend_score": None,
                        "buyer_intent_score": None,
                        "design_score": None,
                        "opportunity_score": None,
                    })

                st.session_state["keyword_results"] = results

            st.success(t["saved"])

        except Exception as error:
            st.error(f"Collection error: {error}")


# Keep collected results during Streamlit reruns.
results = st.session_state.get("keyword_results", [])

st.metric(t["count"], len(results))

if results:

    results_df = pd.DataFrame(results)

    visible_columns = [
        "keyword",
        "niche",
        "trademark_status",
        "competition_level",
        "opportunity_score",
        "amazon_url",
    ]

    visible_columns = [
        col for col in visible_columns
        if col in results_df.columns
    ]

    st.dataframe(
        results_df[visible_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "amazon_url": st.column_config.LinkColumn(
                t["amazon"],
                display_text="Open Amazon",
            )
        },
    )

    warning_count = sum(
        1 for item in results
        if item.get("trademark_status") == "WARNING"
    )

    st.warning(
        f"{t['trademark']}: {warning_count} "
        f"potential warning(s). {t['trademark_warning']}"
    )

    st.divider()

    # ----------------------------------------------
    # Manual competition and opportunity scoring
    # ----------------------------------------------

    st.subheader(t["competition"])
    st.info(t["competition_warning"])

    keyword_options = [
        item["keyword"] for item in results
    ]

    selected_keyword = st.selectbox(
        t["select_keyword"],
        keyword_options,
    )

    with st.form("opportunity_scoring_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            result_count = st.number_input(
                t["result_count"],
                min_value=0,
                max_value=1000000,
                value=0,
                step=100,
            )

        with col2:
            exact_count = st.number_input(
                t["exact_count"],
                min_value=0,
                max_value=1000000,
                value=0,
                step=50,
            )

        with col3:
            average_reviews = st.number_input(
                t["reviews"],
                min_value=0,
                max_value=1000000,
                value=0,
                step=10,
            )

        st.caption(t["score_warning"])

        col4, col5 = st.columns(2)

        with col4:
            demand = st.slider(
                t["demand"],
                0, 100, 50,
            )

            trend = st.slider(
                t["trend"],
                0, 100, 50,
            )

        with col5:
            buyer_intent = st.slider(
                t["intent"],
                0, 100, 50,
            )

            design = st.slider(
                t["design"],
                0, 100, 50,
            )

        submitted = st.form_submit_button(
            t["calculate"]
        )

    if submitted:

        competition = calculate_competition_score(
            result_count=result_count if result_count > 0 else None,
            exact_match_count=exact_count if exact_count > 0 else None,
            average_reviews=average_reviews if average_reviews > 0 else None,
        )

        if competition is None:
            st.error(t["no_competition"])
        else:
            opportunity = calculate_opportunity_score(
                demand_score=demand,
                competition_score=competition,
                trend_score=trend,
                buyer_intent_score=buyer_intent,
                design_score=design,
            )

            for item in results:
                if item["keyword"] == selected_keyword:
                    item.update({
                        "demand_score": demand,
                        "competition_score": competition,
                        "competition_level": get_competition_level(
                            competition
                        ),
                        "trend_score": trend,
                        "buyer_intent_score": buyer_intent,
                        "design_score": design,
                        "opportunity_score": opportunity,
                    })

            st.session_state["keyword_results"] = results

            st.success(
                f"{t['score']}: {opportunity}/100"
            )

            st.metric(
                t["competition"],
                f"{competition}/100",
                get_competition_level(competition),
            )

    # ----------------------------------------------
    # CSV export
    # ----------------------------------------------

    st.divider()
    st.subheader("CSV Export")

    csv_data = export_to_csv(results)

    st.download_button(
        label=t["download"],
        data=csv_data,
        file_name="merch_trend_hunter_keywords.csv",
        mime="text/csv",
    )

else:
    st.info(t["empty"])


# --------------------------------------------------
# Methodology and limitations
# --------------------------------------------------

st.divider()

st.subheader(t["method"])
st.write(t["method_text"])
st.caption(
    "Opportunity scores use manually entered estimates. "
    "Autocomplete suggestions are not search-volume data. "
    "Trademark warnings are not legal clearance. "
    "Amazon result counts are approximate."
)
