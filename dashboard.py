import streamlit as st
import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# connect to Snowflake
def init_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        
    )

st.title("📊 Reddit Analytics Dashboard")

try:
    conn = init_connection()
    cur = conn.cursor()
    query = "SELECT * FROM reddit_db.dbt_transform.daily_posts_count ORDER BY post_date"
    cur.execute(query)
    df = cur.fetch_pandas_all()
    
    col1, col2 = st.columns(2)
    
    col1.metric("total posts", df['TOTAL_POSTS'].sum())
    col2.metric("unique authors", df['UNIQUE_AUTHORS'].sum())
    st.bar_chart(df, x='POST_DATE', y='TOTAL_POSTS', width=600, height=400)

except Exception as e:
    st.error(f"Error: {e}")