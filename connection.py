"""Shared Snowflake connection helper.

Every script imports get_connection() from here so credential / env-var handling
lives in exactly ONE place. This is what prevents the naming drift that broke the
pipeline before (the loader read WAREHOUSE/DATABASE/SCHEMA while the dashboard and
CI used the SNOWFLAKE_-prefixed names).

All variables use the SNOWFLAKE_ prefix. Configure them in a local .env file (for
local runs) or as GitHub Actions secrets (for CI):

    SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
    SNOWFLAKE_ROLE  (optional)
"""

import os

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# Maps the snowflake.connector argument -> the environment variable it comes from.
_REQUIRED = {
    "user": "SNOWFLAKE_USER",
    "password": "SNOWFLAKE_PASSWORD",
    "account": "SNOWFLAKE_ACCOUNT",
    "warehouse": "SNOWFLAKE_WAREHOUSE",
    "database": "SNOWFLAKE_DATABASE",
    "schema": "SNOWFLAKE_SCHEMA",
}


def get_connection():
    """Open and return a Snowflake connection built from SNOWFLAKE_* env vars.

    Raises a clear RuntimeError listing any missing variables, instead of silently
    connecting with None values (which previously produced a confusing
    'No active warehouse selected' error deep in CI).
    """
    params = {arg: os.getenv(var) for arg, var in _REQUIRED.items()}

    missing = [var for arg, var in _REQUIRED.items() if not params[arg]]
    if missing:
        raise RuntimeError(
            "Missing required Snowflake env vars: " + ", ".join(missing)
        )

    role = os.getenv("SNOWFLAKE_ROLE")
    if role:
        params["role"] = role

    return snowflake.connector.connect(**params)


if __name__ == "__main__":
    # Smoke test: `python connection.py` verifies the connection works.
    with get_connection() as conn:
        version = conn.cursor().execute("SELECT current_version()").fetchone()[0]
        print(f"Connection OK - Snowflake {version}")
