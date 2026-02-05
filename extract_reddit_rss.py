import feedparser
import json

rss_url = "https://www.reddit.com/r/dataengineering/new/.rss"
feed = feedparser.parse(rss_url)

data_to_extract = []

for entry in feed.entries:
    post = {
    'title': entry.title,
    'link': entry.link,
    'published': entry.published,
    'author': entry.author
    }
    data_to_extract.append(post)    

try:
    with open('reddit_de_posts.json', 'w') as json_file:
        json.dump(data_to_extract, json_file, indent=4)
        print("Data successfully written to reddit_de_posts.json")

except IOError:
    print("Error writing to file")



