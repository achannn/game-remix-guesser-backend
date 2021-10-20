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
  try:
      page_info = scraper.scrape_remix_page(page_url)
  except:
      raise
  remix = {
    'remix_youtube_url': page_info['remix_youtube_url'],
    'ocremix_remix_url': page_info['ocremix_remix_url'],
    'remix_title': page_info['remix_title'],
    'ocremix_remix_id': ocremixid,
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
  ocremix_mix = db.query(models.Remix).filter_by(ocremix_remix_id=remix['ocremix_remix_id']).first()
  if (ocremix_mix is not None):
      return ocremix_mix
  return crud.deep_create_remix(db, remix, remix_artist, remix_original_song, original_artist, videogame)

@app.get('/remixes/')
def give_remixes(db: Session = Depends(get_db)):
    return crud.get_remixes(db)

@app.get('/game/')
def give_question(db: Session = Depends(get_db)):
    return crud.return_random_question(db)

# @app.get('/question/{question_id}')
# def check_if_answer_correct():

@app.get('/makequestion/')
def generate_question(db: Session = Depends(get_db)):
    return crud.generate_question(db)

@app.get('/seed/')
def seed_db(db: Session = Depends(get_db)):
    ids = [
        "OCR04280",
        "OCR04270",
        "OCR04271",
        "OCR04272",
        "OCR04273",
        "OCR04274",
        "OCR04275",
        "OCR04276",
        "OCR04277",
        "OCR04278",
        "OCR04279",
        "OCR04260",
        "OCR04261",
        "OCR04262",
        "OCR04263",
        "OCR04264",
        "OCR04265",
        "OCR04266",
        "OCR04267",
        "OCR04268",
        "OCR04269",

    ]
    return [consume_ocremix_remix(i, db) for i in ids]
