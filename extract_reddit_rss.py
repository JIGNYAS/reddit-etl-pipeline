"""Extract the newest posts from r/dataengineering's RSS feed to a local JSON file."""

import json
import sys

import feedparser

RSS_URL = "https://www.reddit.com/r/dataengineering/new/.rss"
OUTPUT_FILE = "reddit_de_posts.json"
# Reddit returns 429 / blocks requests that use feedparser's default User-Agent.
USER_AGENT = "reddit-etl-pipeline/1.0 (portfolio project)"


def main():
    feed = feedparser.parse(RSS_URL, agent=USER_AGENT)

    # feedparser never raises on a bad fetch; it sets bozo / leaves entries empty.
    # Fail loudly so the pipeline goes red instead of writing an empty file.
    if feed.bozo:
        raise RuntimeError(f"Failed to parse feed: {feed.bozo_exception}")
    if not feed.entries:
        raise RuntimeError("Feed returned 0 entries (rate-limited or blocked?)")

    posts = [
        {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "author": entry.author,
        }
        for entry in feed.entries
    ]

    with open(OUTPUT_FILE, "w") as json_file:
        json.dump(posts, json_file, indent=4)

    print(f"Extracted {len(posts)} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Extraction failed: {e}", file=sys.stderr)
        sys.exit(1)
