import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from typing import List
import csv

from . import crud, models, schemas, internal
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

# @app.get('/seed/')
def consume_ocremix_remix(db_session, row: List[str]):
  internal.log_info('invoked consume_ocremix_ with row {row}')

  remix = {
    'remix_youtube_url': row[0],
    'ocremix_remix_url': row[1],
    'remix_title': row[2],
    'ocremix_remix_id': row[3],
  }
  remix_artist = {
    'remix_artist_name': row[4],
    'remix_artist_ocremix_url': row[5],
  }
  remix_original_song = {
    'original_song_title': row[6],
    'original_song_ocremix_url': row[7],
  }
  original_artist = {
    'original_artist_name': row[8],
    'original_artist_ocremix_url': row[9],
  }
  videogame = {
    'videogame_title': row[10],
    'videogame_ocremix_url': row[11],
    # 'videogame_console': row.videogame_console,
  }
  ocremix_mix = db_session.query(models.Remix).filter_by(ocremix_remix_id=remix['ocremix_remix_id']).first()
  if (ocremix_mix is not None):
      return ocremix_mix
  out = crud.deep_create_remix(db_session, remix, remix_artist, remix_original_song, original_artist, videogame)
  return out

def parse_csv():
    internal.log_info(f'About to open csv')
    db_session_maker = sessionmaker(bind=engine)
    db_session = db_session_maker()
    with open('ocremix.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            internal.log_info('row count ' + str(line_count))
            consume_ocremix_remix(db_session, row)
            line_count += 1

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




parse_csv()
