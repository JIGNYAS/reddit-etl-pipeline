WITH staging AS (
    SELECT * FROM {{ ref('stg_reddit_posts')}}
)

SELECT 
    DATE(published_date) AS post_date,
    COUNT(*) AS total_posts,
    COUNT(DISTINCT author) AS unique_authors
FROM staging
GROUP BY 1
ORDER BY 1 DESC