-- One-time Snowflake setup for the Reddit ETL pipeline.
-- All statements use IF NOT EXISTS so this script is safe to re-run.

CREATE WAREHOUSE IF NOT EXISTS reddit_wh
WITH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  COMMENT = 'Warehouse for Reddit ETL pipeline';

CREATE DATABASE IF NOT EXISTS reddit_db;

CREATE SCHEMA IF NOT EXISTS reddit_db.raw;

CREATE TABLE IF NOT EXISTS reddit_db.raw.reddit_posts (raw_data VARIANT);
