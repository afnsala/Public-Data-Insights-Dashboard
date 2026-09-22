"""
app.py

Streamlit dashboard for exploring the dataset.

Run with: streamlit run app.py
"""

import streamlit as st
import plotly.express as px
from pathlib import Path

import queries

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PAGE_TITLE = "US Corn Acres Planted Dashboard"
DATE_COLUMN = "year"          # column representing time, for trend charts
VALUE_COLUMN = "value"        # main numeric column to analyze
CATEGORY_COLUMN = "category"  # report period type (final estimate vs. forecasts)

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(page_title=PAGE_TITLE, layout="wide")
st.title(PAGE_TITLE)
st.caption("Built with Python, SQLite/SQL, and Streamlit")

if not Path(queries.DB_PATH).exists():
    st.error(
        f"Couldn't find {queries.DB_PATH}. Run `python data_pipeline.py` "
        f"first to build the database from your raw dataset."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------

st.sidebar.header("Filters")

try:
    category_options = queries.get_distinct_values(CATEGORY_COLUMN)
    selected_category = st.sidebar.selectbox(
        f"Filter by {CATEGORY_COLUMN}", ["All"] + category_options
    )
except Exception as e:
    st.sidebar.warning(f"Couldn't load filter options: {e}")
    selected_category = "All"

filters = {}
if selected_category != "All":
    filters[CATEGORY_COLUMN] = selected_category

# ---------------------------------------------------------------------------
# Summary stats row
# ---------------------------------------------------------------------------

try:
    stats = queries.get_summary_stats(VALUE_COLUMN)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{int(stats['count']):,}")
    col2.metric(f"Avg {VALUE_COLUMN}", f"{stats['mean']:.2f}")
    col3.metric(f"Min {VALUE_COLUMN}", f"{stats['min']:.2f}")
    col4.metric(f"Max {VALUE_COLUMN}", f"{stats['max']:.2f}")
except Exception as e:
    st.warning(f"Couldn't compute summary stats \u2014 check your column config. ({e})")

st.divider()

# ---------------------------------------------------------------------------
# Trend chart
# ---------------------------------------------------------------------------

st.subheader("Trend Over Time")
try:
    trend_df = queries.get_trend_over_time(DATE_COLUMN, VALUE_COLUMN, group_by=CATEGORY_COLUMN)
    if selected_category != "All":
        trend_df = trend_df[trend_df[CATEGORY_COLUMN] == selected_category]
    fig = px.line(
        trend_df, x=DATE_COLUMN, y="avg_value", color=CATEGORY_COLUMN
        if selected_category == "All" else None,
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"Couldn't build trend chart \u2014 check DATE_COLUMN/VALUE_COLUMN config. ({e})")

# ---------------------------------------------------------------------------
# Comparison view
# ---------------------------------------------------------------------------

# adjust categories so that the top 10 are always shown, even if a filter is applied.
# make them not stack and rather seperate the bars for better comparison.
# search up how to seperate bars in plotly express bar chart and implement it.

st.subheader(f"Top {CATEGORY_COLUMN} by {VALUE_COLUMN}")
try:
    top_df = queries.get_top_n(CATEGORY_COLUMN, VALUE_COLUMN, n=10)
    fig2 = px.bar(top_df, x=CATEGORY_COLUMN, y=VALUE_COLUMN)
    st.plotly_chart(fig2, use_container_width=True)
except Exception as e:
    st.warning(f"Couldn't build comparison chart \u2014 check column config. ({e})")

# ---------------------------------------------------------------------------
# Filterable data table
# ---------------------------------------------------------------------------

st.subheader("Explore the Data")
try:
    data_df = queries.get_filtered_records(filters)
    st.dataframe(data_df, use_container_width=True)
    st.caption(f"Showing {len(data_df):,} rows")
except Exception as e:
    st.warning(f"Couldn't load data table: {e}")

# ---------------------------------------------------------------------------
# Insights panel
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Key Insights")
st.markdown(
    """
    *Replace this section with 2-3 written takeaways once you've explored
    your actual dataset. "translating data into
    recommendations" piece 

    - **Insight 1:** ...
    - **Insight 2:** ...
    - **Insight 3:** ...
    """
)
