import os

import streamlit as st

from connection import get_connection

# dbt builds models into the database/schema from its profile, which read the same
# SNOWFLAKE_* env vars. Reading them here (instead of a hardcoded "dbt_transform"
# schema that nothing creates) guarantees the dashboard points at what dbt built.
DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

st.title("📊 Reddit Analytics Dashboard")

try:
    conn = get_connection()
    cur = conn.cursor()

    df = cur.execute(
        f"SELECT * FROM {DATABASE}.{SCHEMA}.daily_posts_count ORDER BY post_date"
    ).fetch_pandas_all()

    # True distinct authors over the whole period. Summing the mart's per-day
    # UNIQUE_AUTHORS would double-count anyone active on more than one day.
    unique_authors = cur.execute(
        f"SELECT COUNT(DISTINCT author) FROM {DATABASE}.{SCHEMA}.stg_reddit_posts"
    ).fetchone()[0]

    col1, col2 = st.columns(2)
    col1.metric("Total posts", int(df["TOTAL_POSTS"].sum()))
    col2.metric("Unique authors", int(unique_authors))
    st.bar_chart(df, x="POST_DATE", y="TOTAL_POSTS", width=600, height=400)

except Exception as e:
    st.error(f"Error: {e}")
