import navi_internal
import feedparser
from datetime import datetime, timedelta
import pytz
import requests
from urllib.parse import urlparse

command: str = "navi-tic"
use: str = "Gather cybersec news from RSS feeds"
aliases: list = ['threat intelligence', 'cybersec news', 'cybersecurity news', 'threat intel']
params: dict = {
    '-help': f'{use}',
    '-h': f'{use}',
}

help_params: tuple = ('-help', '-h')

def print_params() -> None:
    print(f"{'Parameter':<10} | {'Description'}")
    print("-" * 40)

    for param, description in params.items():
        print(f"{param:<10} | {description}")

def shorten_url(url: str) -> str:
    try:
        response = requests.get(f'http://tinyurl.com/api-create.php?url={url}')
        return response.text
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return url

def get_source_name(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

def run(arguments=None) -> None:
    navi_instance = navi_internal.navi_instance
    navi_instance.print_message(f"Gathering threat intelligence news...")

    if arguments.text.lower() in ['help', '-h', '-help']:
        print_params()
        return

    feeds = [
        'https://www.reddit.com/r/cybersecurity/.rss',
    ]

    entries = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            try:
                published = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                try:
                    published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%S%z')
                except ValueError:
                    continue

            if published > datetime.now(pytz.utc) - timedelta(days=1):
                entries.append({
                    'source': get_source_name(feed),
                    'title': entry.title,
                    'link': entry.link,
                    'published': published
                })

    if not entries:
        navi_instance.print_message("No new threat intelligence news found.")
    else:
        navi_instance.print_message("Here are some recent threat intelligence news articles:\n")
        for entry in sorted(entries, key=lambda x: x['published'], reverse=True):
            print(f"{entry['source']}: {entry['title']}\n{entry['link']}\n")