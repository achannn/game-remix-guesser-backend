import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
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



@app.get('/remixes/{id}' )
def get_remix_by_id(ocremix_id: str, db: Session = Depends(get_db)):
    return crud.get_remix_by_ocremix_id(db, ocremix_id=ocremix_id)

@app.get('remixes/create/{id}')
def get_or_create_remix_by_id(ocremix_id: str, db: Session = Depends(get_db)):
    internal.log_info(f"get or create {ocremix_id}")
    remix = get_remix_by_id(ocremix_id=ocremix_id, db=db)
    if remix is not None:
        internal.log_info(f"already had {ocremix_id}")
        return remix
    internal.log_info(f"preparing to create {id}")
    return consume_ocremix_remix(ocremix_id, db)


@app.get('/parse/{ocremixid}')
def consume_ocremix_remix(ocremixid: str, db: Session = Depends(get_db)):
  page_url = f"https://ocremix.org/remix/{ocremixid}"
  internal.log_info(f"GET to /parse with {ocremixid}")
  try:
      page_info = scraper.scrape_remix_page(page_url)
  except:
      internal.log_error(f"Failed to get page {page_url}")
      return None

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

@app.get('/game/', response_model=models.QuestionPackage)
def give_question(db: Session = Depends(get_db)):
    return crud.generate_question(db)

@app.post('/game/', response_model=models.CorrectAnswerPackage or None)
def check_answer(db: Session = Depends(get_db), answer: models.Answer = {}):
    found_answer = crud.match_public_id_to_secret_id(db=db, public_id=answer.public_id, secret_id=answer.secret_id)
    if found_answer is None:
        return None;
    answer_package = models.CorrectAnswerPackage(
        origin_game=found_answer.remix_original_song.original_song_videogame.videogame_title,
        remix_artist=found_answer.remix_artists.remix_artist_name,
        ocremix_remix_url=found_answer.ocremix_remix_url,
        original_song_title=found_answer.remix_original_song.original_song_title
    )

    return answer_package

@app.get('/seed/')
def seed_db(db: Session = Depends(get_db)):
    ids = internal.ids
    internal.log_info("beginning seed")
    result = [get_or_create_remix_by_id(ocremix_id=i, db=db) for i in ids]
    internal.log_info("finished seed")
    return {"status": "ok"}

static_app = FastAPI(title="Static Files")
static_app.mount("/api", app)
static_app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
