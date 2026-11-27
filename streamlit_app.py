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


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Merch Trend Hunter",
    page_icon="🎯",
    layout="wide",
)

DATA = Path("data/trends.json")


# --------------------------------------------------
# Interface translations
# --------------------------------------------------

TEXT = {
    "English": {
        "subtitle": "US market research for print-on-demand designers",
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
        "result_count": "Approximate Amazon result count (manual)",
        "filter_results": "Filter keywords",
        "filtered_count": "Keywords with 0–99 results",
        "exact_count": "Approximate exact-match count",
        "reviews": "Average reviews observed",
        "calculate": "Save count and calculate opportunity score",
        "download": "Download CSV",
        "warning": "Autocomplete suggestions are not search volume or sales data.",
        "score_warning": "Scores based on manual estimates are research aids, not verified market measurements.",
        "trademark_warning": "No match does not mean legally safe. This is not legal clearance.",
        "competition_warning": "Enter competition indicators from your own Amazon observations. Result counts are approximate.",
        "saved": "Keywords collected successfully.",
        "no_competition": "The result count was saved. Enter at least one additional competition indicator to calculate a score.",
        "select_keyword": "Select a keyword to evaluate",
        "amazon": "Amazon USA search",
        "niche": "Niche",
        "status": "Trademark status",
        "opportunity": "Opportunity",
        "method": "About this tool",
        "method_text": "Google Trends shows trending searches. Amazon Autocomplete provides keyword suggestions. Neither source proves product sales. Amazon result counts must be entered manually.",
        "last": "Last collection",
        "source": "Source",
        "tracked": "Tracked trends",
        "published": "Published",
        "traffic": "Google traffic label",
        "no_trends": "No trend data saved yet. Run the GitHub Actions workflow.",
        "collect_error": "Keyword collection failed. Please try again later.",
        "no_filtered": "No keywords currently have a saved result count from 0 to 99. Enter the approximate Amazon result count in the analysis section below.",
        "trademark_matches": "Matched terms",
        "all_keywords": "All collected keywords",
    },
    "العربية": {
        "subtitle": "أبحاث السوق الأمريكي لمصممي الطباعة عند الطلب",
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
        "result_count": "عدد نتائج Amazon التقريبي (إدخال يدوي)",
        "filter_results": "تصفية الكلمات",
        "filtered_count": "الكلمات التي نتائجها من 0 إلى 99",
        "exact_count": "عدد النتائج المطابقة التقريبي",
        "reviews": "متوسط مراجعات المنتجات التي شاهدتها",
        "calculate": "حفظ العدد وحساب نقاط الفرصة",
        "download": "تحميل ملف CSV",
        "warning": "اقتراحات البحث لا تمثل حجم البحث أو المبيعات الفعلية.",
        "score_warning": "النقاط المبنية على تقديرات يدوية هي أداة مساعدة وليست قياسات سوق مؤكدة.",
        "trademark_warning": "عدم وجود تطابق لا يعني أن الاستخدام آمن قانونيًا. هذا ليس فحصًا قانونيًا.",
        "competition_warning": "أدخل مؤشرات المنافسة التي رصدتها بنفسك في Amazon. أعداد النتائج تقريبية.",
        "saved": "تم جمع الكلمات بنجاح.",
        "no_competition": "تم حفظ عدد النتائج. أدخل مؤشر منافسة إضافيًا واحدًا على الأقل لحساب النقاط.",
        "select_keyword": "اختر كلمة لتحليلها",
        "amazon": "بحث Amazon USA",
        "niche": "المجال",
        "status": "حالة العلامة التجارية",
        "opportunity": "الفرصة",
        "method": "حول الأداة",
        "method_text": "يعرض Google Trends عمليات البحث الرائجة، ويقدم Amazon Autocomplete اقتراحات كلمات. لا يثبت أي منهما مبيعات المنتجات. يجب إدخال عدد نتائج Amazon يدويًا.",
        "last": "آخر جمع",
        "source": "المصدر",
        "tracked": "الترندات المرصودة",
        "published": "تاريخ النشر",
        "traffic": "مؤشر زيارات Google",
        "no_trends": "لا توجد بيانات ترند محفوظة بعد. شغّل سير العمل من GitHub Actions.",
        "collect_error": "فشل جمع الكلمات. حاول مرة أخرى لاحقًا.",
        "no_filtered": "لا توجد حاليًا كلمات محفوظ لها عدد نتائج من 0 إلى 99. أدخل عدد نتائج Amazon التقريبي في قسم التحليل أدناه.",
        "trademark_matches": "المصطلحات المطابقة",
        "all_keywords": "جميع الكلمات المجموعة",
    },
}


# --------------------------------------------------
# Sidebar and language
# --------------------------------------------------

with st.sidebar:
    st.title("🎯 Merch Trend Hunter")
    lang = st.radio("Language / اللغة", ["English", "العربية"])
    st.divider()
    st.write("🇺🇸 United States")
    st.caption("Version 0.3.1")

t = TEXT[lang]

st.title("🎯 Merch Trend Hunter")
st.caption(t["subtitle"])
st.info(t["warning"], icon="ℹ️")


# --------------------------------------------------
# Google Trends section
# --------------------------------------------------

st.header(t["trends"])

try:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
except (FileNotFoundError, json.JSONDecodeError, OSError):
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

    visible_trend_columns = [
        col for col in ["Trend", t["traffic"], t["published"]]
        if col in trend_df.columns
    ]

    if visible_trend_columns:
        st.dataframe(
            trend_df[visible_trend_columns],
            use_container_width=True,
            hide_index=True,
        )
else:
    st.warning(t["no_trends"])


# --------------------------------------------------
# Amazon keyword collection
# --------------------------------------------------

st.divider()
st.header(t["keywords"])

if "keyword_results" not in st.session_state:
    st.session_state["keyword_results"] = []

default_seeds = "\n".join(DEFAULT_SEEDS)

with st.form("keyword_collection_form"):
    seeds_text = st.text_area(
        t["seeds"],
        value=default_seeds,
        height=150,
    )
    limit_per_seed = st.number_input(
        t["limit"],
        min_value=1,
        max_value=20,
        value=10,
        step=1,
    )
    collect_submitted = st.form_submit_button(t["collect"])

if collect_submitted:
    seed_keywords = [
        seed.strip()
        for line in seeds_text.splitlines()
        for seed in line.split(",")
        if seed.strip()
    ]

    if not seed_keywords:
        st.error(t["seeds"])
    else:
        try:
            with st.spinner(t["collect"] + "..."):
                collected = collect_keywords(
                    seed_keywords=seed_keywords,
                    limit_per_seed=int(limit_per_seed),
                )

            prepared_results = []
            for item in collected:
                keyword = item.get("keyword", "").strip()
                if not keyword:
                    continue

                trademark_result = check_trademark(keyword)
                item.update(trademark_result)
                item["amazon_url"] = build_amazon_shirt_url(keyword)

                # Amazon result counts are not supplied by Autocomplete.
                # The user enters this value manually in the analysis form.
                item.setdefault("result_count", None)
                prepared_results.append(item)

            st.session_state["keyword_results"] = prepared_results
            if prepared_results:
                st.success(f"{t['saved']} ({len(prepared_results)})")
            else:
                st.warning(t["empty"])

        except Exception as error:
            st.error(f"{t['collect_error']} {error}")


# --------------------------------------------------
# Keep collected results during Streamlit reruns
# --------------------------------------------------

results = st.session_state.get("keyword_results", [])
st.metric(t["count"], len(results))


# --------------------------------------------------
# Manual competition and opportunity scoring
# --------------------------------------------------

if results:
    st.divider()
    st.subheader(t["competition"])
    st.info(t["competition_warning"])

    keyword_options = [item["keyword"] for item in results]

    selected_keyword = st.selectbox(
        t["select_keyword"],
        keyword_options,
    )

    selected_item = next(
        (item for item in results if item["keyword"] == selected_keyword),
        {},
    )

    current_result_count = selected_item.get("result_count")
    if current_result_count is None:
        current_result_count = 0

    with st.form("opportunity_scoring_form"):
        result_count = st.number_input(
            t["result_count"],
            min_value=0,
            max_value=1000000,
            value=int(current_result_count),
            step=1,
            key=f"result_count_{selected_keyword}",
        )

        col1, col2 = st.columns(2)

        with col1:
            exact_count = st.number_input(
                t["exact_count"],
                min_value=0,
                max_value=1000000,
                value=0,
                step=1,
            )

        with col2:
            average_reviews = st.number_input(
                t["reviews"],
                min_value=0,
                max_value=1000000,
                value=0,
                step=1,
            )

        st.caption(t["score_warning"])

        col3, col4 = st.columns(2)

        with col3:
            demand = st.slider(t["demand"], 0, 100, 50)
            trend = st.slider(t["trend"], 0, 100, 50)

        with col4:
            buyer_intent = st.slider(t["intent"], 0, 100, 50)
            design = st.slider(t["design"], 0, 100, 50)

        submitted = st.form_submit_button(t["calculate"])

    if submitted:
        # Save the result count even when no other competition indicator
        # has been entered. This makes the 0-99 filter usable.
        for item in results:
            if item["keyword"] == selected_keyword:
                item["result_count"] = int(result_count)

        competition = calculate_competition_score(
            result_count=int(result_count),
            exact_match_count=exact_count if exact_count > 0 else None,
            average_reviews=average_reviews if average_reviews > 0 else None,
        )

        if competition is not None:
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
                        "competition_level": get_competition_level(competition),
                        "trend_score": trend,
                        "buyer_intent_score": buyer_intent,
                        "design_score": design,
                        "opportunity_score": opportunity,
                    })

            st.success(f"{t['score']}: {opportunity}/100")
            st.metric(
                t["competition"],
                f"{competition}/100",
                get_competition_level(competition),
            )
        else:
            st.info(t["no_competition"])

        st.session_state["keyword_results"] = results


    # --------------------------------------------------
    # Filter: Amazon result count from 0 to 99
    # --------------------------------------------------

    filtered_results = [
        item for item in results
        if item.get("result_count") is not None
        and 0 <= int(item["result_count"]) <= 99
    ]

    st.divider()
    st.subheader(t["filter_results"])
    st.metric(t["filtered_count"], len(filtered_results))

    if filtered_results:
        results_df = pd.DataFrame(filtered_results)

        visible_columns = [
            "keyword",
            "niche",
            "result_count",
            "trademark_status",
            "matched_terms",
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
            1 for item in filtered_results
            if item.get("trademark_status") == "WARNING"
        )
        st.warning(
            f"{t['trademark']}: {warning_count}. "
            f"{t['trademark_warning']}"
        )
    else:
        st.info(t["no_filtered"])

    # --------------------------------------------------
    # CSV export: filtered keywords only
    # --------------------------------------------------

    st.divider()
    st.subheader("CSV Export")

    csv_data = export_to_csv(filtered_results)

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
    "Amazon result counts are approximate and entered manually."
)
