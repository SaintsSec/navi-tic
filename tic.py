import requests
from bs4 import BeautifulSoup 
from navi import get_parameters
from navi_shell import print_message


command = "navi-tic"
use = "Navi Threat Intelligence"
aliases = ['--tic', '--ntic']

# Define the RSS feed URL and its title
RSS_FEED_URL = ["https://feeds.cisco.com/talus/rss"]
RSS_FEED_TITLE = "Navi - Threat Feed"

def get_rss_titles_and_excerpts():
    # Send a GET request to the RSS feed URL
    response = requests.get(RSS_FEED_URL)

    # Parse the RSS feed using BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')

    # Get the latest 5 items from the RSS feed
    items = soup.find_all('item')
    latest_items = items[-5:]

    # Extract the title and excerpt for each item
    titles_and_excerpts = []
    for item in latest_items:
        title = item.find('title').text.strip()
        excerpt = item.find('description').text.strip()
        titles_and_excerpts.append((title, excerpt))

    return titles_and_excerpts


def run(arguments=None):
    titles_and_excerpts = get_rss_titles_and_excerpts()

    # Print the latest 5 RSS feed titles and excerpts
    print_message(f"{RSS_FEED_TITLE} Latest Titles and Excerpts:")
    for title, excerpt in titles_and_excerpts:
        print_message(f"Title: {title}\nExcerpt: {excerpt}\n")  
