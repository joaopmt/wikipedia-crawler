"""
Goes from starting_url trough multiple Wikipedia's articles
by folowing the first link to another article in each article's
main text (it avoids foot notes links, pronunciation links and
such). Stops when target_url has been reached or article chain
has reached MAX_CHAIN_SIZE limit or a cycle is detected or a
no-link article is reached.
"""

import time

import requests
from bs4 import BeautifulSoup

MAX_CHAIN_SIZE = 20
starting_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def continue_crawl(search_history, target_url, max_steps=25):
    """
    Returns True if the crawl should continue, False otherwise.
    """
    if len(search_history) >= max_steps:
        return False
    if search_history[-1] == target_url:
        print(target_url+" has been reached (target article).")
        return False
    if search_history[-1] in search_history[:-1]:
        print("Cicle detected.")
        return False
    return True

def find_first_link(url):
    """
    Find, extract and return the first link to another article
    in current article's main text
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    first_link = None
    # Iterate over main content direct childs and get first link to another article from first <p> tag
    for child in soup.find(id="mw-content-text").find(class_="mw-parser-output").find_all("p", recursive=False):
        if child.find("a", recursive=False):
            first_link = child.find("a", recursive=False).get("href")
            break
    # If there is no link in article's main text
    if not first_link:
        return None
    return "https://en.wikipedia.org" + first_link

next_url = starting_url
visited_urls = [starting_url]
while continue_crawl(visited_urls, target_url, MAX_CHAIN_SIZE):
    next_url = find_first_link(next_url)
    if next_url is None:
        print("No-link article detected.")
        break
    visited_urls.append(next_url)
    # respect wikipedia's bot policy
    time.sleep(2)
    
for url in visited_urls:
    print(url)
