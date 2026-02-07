-- models/staging/stg_reddit_posts.sql

with source as (
    select * from {{ source('reddit', 'reddit_posts') }}
),

renamed as (
    select
        raw_data:title::string as title,
        raw_data:author::string as author,
        raw_data:domain::string as domain,
        raw_data:link::string as post_url,
        raw_data:published::string as published_raw,
        try_to_timestamp(raw_data:published::string) as published_date
    from source
)

select * from renamed
-- This allows us to group by URL and pick the 1st row
QUALIFY ROW_NUMBER() OVER (PARTITION BY post_url ORDER BY published_date DESC) = 1