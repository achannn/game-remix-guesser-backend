from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schema, scraper
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


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


@app.get('/parse/{ocremixid}', response_model=schemas.Remix)
def consume_ocremix_remix(ocremixid: str, db: Session = Depends(get_db)):
  page_url = f"https://ocremix.org/remix/{ocremixid}"
  page_info = scraper.scrame_remix_page(page_url)
  remix = {
    'remix_youtube_url': page_info.remix_youtube_url,
    'ocremix_remix_url': page_info.ocremix_remix_url,
    'remix_title': page_info.remix_title,
  }
  remix_artist = {
    'remix_artist_name': page_info.remix_artist_name,
    'remix_arist_ocremix_url': page_info.remix_artist_ocremix_url,
  }
  remix_original_song = {
    'original_song_title': page_info.original_song_title,
    'original_song_ocremix_url': page_info.original_song_ocremix_url,
  }
  original_artist = {
    'original_artist_name': page_info.original_artist_name,
    'original_artist_ocremix_url': page_info.original_artist_ocremix_url,
  }
  videogame = {
    'videogame_title': page_info.videogame_title,
    'videogame_ocremix_url': page_info.videogame_ocremix_url,
    # 'videogame_console': page_info.videogame_console,
  }

  return crud.deep_create_remix(db, remix, remix_artist, remix_original_song, original_artist, videogame)
