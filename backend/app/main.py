import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas, scraper, internal
from .database import SessionLocal, engine, Base


retries = 5
def initiate_connection(retries: int):
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as inst:
        internal.log_error(f"db connection {retries} failed because {inst}")
        if retries > 0:
            internal.log_error('Trying to reconnect')
            retries = retries - 1
            time.sleep(4)
            initiate_connection(retries)
        else:
            internal.log_error('Failed to reconnect, giving up.')

initiate_connection(retries)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    )

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/')
def main():
  return 'Hello, Docker!'


@app.get('/parse/{ocremixid}')
def consume_ocremix_remix(ocremixid: str, db: Session = Depends(get_db)):
  page_url = f"https://ocremix.org/remix/{ocremixid}"
  page_info = scraper.scrape_remix_page(page_url)
  remix = {
    'remix_youtube_url': page_info['remix_youtube_url'],
    'ocremix_remix_url': page_info['ocremix_remix_url'],
    'remix_title': page_info['remix_title'],
  }
  remix_artist = {
    'remix_artist_name': page_info['remix_artist_name'],
    'remix_artist_ocremix_url': page_info['remix_artist_ocremix_url'],
  }
  remix_original_song = {
    'original_song_title': page_info['original_song_title'],
    'original_song_ocremix_url': page_info['original_song_ocremix_url'],
  }
  original_artist = {
    'original_artist_name': page_info['original_artist_name'],
    'original_artist_ocremix_url': page_info['original_artist_ocremix_url'],
  }
  videogame = {
    'videogame_title': page_info['videogame_title'],
    'videogame_ocremix_url': page_info['videogame_ocremix_url'],
    # 'videogame_console': page_info.videogame_console,
  }
  return crud.deep_create_remix(db, remix, remix_artist, remix_original_song, original_artist, videogame)
