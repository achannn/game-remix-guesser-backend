import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_page(url: str):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return page

def get_soup(page):
    return BeautifulSoup(page, "html.parser")

def scrape_remix_page(url):
    soup = get_soup(get_page(url))
    song_info = soup.find("h1").contents
    game_title = song_info[2].contents[0]
    game_url = soup.find("h1").find("a")['href']
    remix_title = song_info[3]
    remix_url = url
    original_song_title = soup.find('h3').contents[1].contents
    original_song_ocremix_url = soup.find('h3').find('a')['href']
    remix_author = soup.find('h2').contents[1].contents[0]
    remix_author_ocremix_url = soup.find('h2').find('a')['href']
    original_song_artist = soup.find('a', class_='color-original').contents[0]
    original_song_artist_url = soup.find('a', class_='color-original')['href']
