from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv()

USER = os.getenv('SNOWFLAKE_USER')
PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
WAREHOUSE = os.getenv('WAREHOUSE')
DATABASE = os.getenv('DATABASE')
SCHEMA = os.getenv('SCHEMA')
ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')

try:
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA )
    print("connection established")

    cur = conn.cursor()
    sql_query = "SELECT current_version()"
    cur.execute(sql_query)
    print(cur.fetchone())
    

except Exception as e:
    print(f"Unsuccessful with this error {e}")