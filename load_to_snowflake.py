"""Load extracted Reddit posts from the local JSON file into the Snowflake raw table."""

import json
import sys

from connection import get_connection

INPUT_FILE = "reddit_de_posts.json"
INSERT_SQL = "INSERT INTO reddit_db.raw.reddit_posts (raw_data) SELECT PARSE_JSON(%s)"


def main():
    with open(INPUT_FILE, "r") as json_file:
        posts = json.load(json_file)

    conn = get_connection()
    try:
        cur = conn.cursor()
        for post in posts:
            # Bound parameter (not string concat) -> no SQL injection / quoting bugs.
            cur.execute(INSERT_SQL, (json.dumps(post),))
        conn.commit()
        print(f"Loaded {len(posts)} posts to Snowflake")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Exit non-zero so a failed load turns the CI job RED instead of
        # printing an error and reporting success.
        print(f"Load failed: {e}", file=sys.stderr)
        sys.exit(1)
