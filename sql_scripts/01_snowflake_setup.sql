CREATE WAREHOUSE reddit_wh  -- Create OR REPLACE WAREHOUSE reddit_wh use this only once to avoid dropping the warehouse and losing data
WITH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  COMMENT = 'Warehouse for Reddit ETL pipeline';

CREATE reddit_db; -- Create OR REPLACE reddit_db use this only once to avoid dropping the database and losing data

CREATE SCHEMA reddit_db.raw; -- Create OR REPLACE SCHEMA reddit_db.raw use this only once to avoid dropping the schema and losing data

CREATE reddit_db.raw.reddit_posts( raw_data VARIANT); -- Create OR REPLACE reddit_db.raw.reddit_posts use this only once to avoid dropping the table and losing data