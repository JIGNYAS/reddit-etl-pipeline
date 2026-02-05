from dotenv import load_dotenv
import os
import snowflake.connector
import json

load_dotenv()

USER = os.getenv('SNOWFLAKE_USER')
PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
WAREHOUSE = os.getenv('WAREHOUSE')
DATABASE = os.getenv('DATABASE')
SCHEMA = os.getenv('SCHEMA')
ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')


try:
    with open('reddit_de_posts.json','r') as json_file:
        data = json.load(json_file)

        conn = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA )
        cur = conn.cursor()
        
        for post in data:

            json_string = json.dumps(post)
            sql_query = "INSERT INTO reddit_db.raw.reddit_posts (raw_data) SELECT PARSE_JSON(%s)"
            cur.execute(sql_query,(json_string,))
        
        conn.commit()
        print("Data successfully loaded to Snowflake")
        
except Exception as e:
    print(f"Error : {e}")

finally:
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error closing connection: {e}")