from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from . import internal

def get_page(url: str):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return page

def get_soup(page):
    return BeautifulSoup(page, "html.parser")

def scrape_remix_page(url):
    try :
        soup = get_soup(get_page(url))
    except Exception as inst:
        internal.log_error(f"Issue getting soup for {url}, error is {inst}")

    song_info = soup.find("h1")

    if song_info is None:
        internal.log_error(f"Can't find song info for {url}")
        return None

    song_info = song_info.contents

    try:
        game_title = song_info[2].contents[0]
    except Exception as inst:
        internal.log_error(f"Issue getting game title for {url}, error is {inst}")

    try:
        game_url = soup.find("h1").find("a")['href']
    except Exception as inst:
        internal.log_error(f"Issue getting game url for {url}, error is {inst}")

    try:
        remix_title = song_info[3]
    except Exception as inst:
        internal.log_error(f"Issue getting remix title for {url}, error is {inst}")


    try:
        original_song_title = soup.find('h3').contents[1].contents[0]
    except Exception as inst:
        internal.log_error(f"Issue getting original song title for {url}, error is {inst}")

    try:
        original_song_ocremix_url = soup.find('h3').find('a')['href']
    except Exception as inst:
        internal.log_error(f"Issue getting original song ocremix url for {url}, error is {inst}")

    try:
        remix_author = soup.find('h2').contents[1].contents[0]
    except Exception as inst:
        internal.log_error(f"Issue getting remix author for {url}, error is {inst}")

    try:
        remix_author_ocremix_url = soup.find('h2').find('a')['href']
    except Exception as inst:
        internal.log_error(f"Issue getting remix author ocremix url for {url}, error is {inst}")

    try:
        original_song_artist = soup.find('a', class_='color-original').contents[0]
    except Exception as inst:
        internal.log_error(f"Issue getting original song artist for {url}, error is {inst}")

    try:
        original_song_artist_url = soup.find('a', class_='color-original')['href']
    except Exception as inst:
        internal.log_error(f"Issue getting original song artist url for {url}, error is {inst}")

    try:
        options = Options()
        options.page_load_strategy = 'normal'
        options.add_argument('--profile-directory=Default')
        options.add_argument('--user-data-dir=~/.config/google-chrome')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        remix_youtube_url_full = driver.find_element_by_id('player3').get_attribute('src')
        remix_youtube_url_parsed = urlparse(remix_youtube_url_full)
        remix_youtube_url = remix_youtube_url_parsed.netloc + remix_youtube_url_parsed.path

    except Exception as inst:
        internal.log_error(f"Issue getting youtube url for {url}, error is {inst}")

    return {
        'ocremix_remix_url': url,
        'videogame_title': game_title,
        'videogame_ocremix_url': game_url,
        'remix_title': remix_title,
        'original_song_title': original_song_title,
        'original_song_ocremix_url': original_song_ocremix_url,
        'remix_artist_name': remix_author,
        'remix_artist_ocremix_url': remix_author_ocremix_url,
        'original_artist_name': original_song_artist,
        'original_artist_ocremix_url': original_song_artist_url,
        'remix_youtube_url': remix_youtube_url,
    }
