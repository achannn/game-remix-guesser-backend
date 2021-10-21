from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from fastapi import Depends
from sqlalchemy.orm import relationship, Session
from .database import SessionLocal, Base, engine
from random import randint
from pydantic import BaseModel
from typing import List

# https://stackoverflow.com/questions/38754816/sqlalchemy-random-unique-integer
def random_remix_public_id():
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    # possibility of same random number is very low.
    # but if you want to make sure, here you can check id exists in database.
    from sqlalchemy.orm import sessionmaker
    db_session_maker = sessionmaker(bind=engine)
    db_session = db_session_maker()
    while db_session.query(Remix).filter(Remix.public_id == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand

def random_remix_secret_id():
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    # possibility of same random number is very low.
    # but if you want to make sure, here you can check id exists in database.
    from sqlalchemy.orm import sessionmaker
    db_session_maker = sessionmaker(bind=engine)
    db_session = db_session_maker()
    while db_session.query(Remix).filter(Remix.secret_id == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand



class Remix(Base):
    __tablename__ = "remixes"

    id = Column(Integer, primary_key=True, index=True)
    ocremix_remix_id = Column(String(20), index=True)
    remix_youtube_url = Column(String(600), index=True)
    ocremix_remix_url = Column(String(600), index=True)
    remix_title = Column(String(600), index=True)
    remix_artist_id = Column(ForeignKey('remix_artists.id'))
    remix_original_song_id = Column(ForeignKey('original_songs.id'))

    # These are for the concept of a "question"
    # Four Remixes will be chosen for the client, along with their public_id
    # One of those Remixes will also be sent separately with only their youtube url and secret_id
    # To know which is right, client will need to send public_id and secret_id
    # Then I guess Ill do something like select where public_id = x and secret_id = y
    public_id = Column(Integer, default=random_remix_public_id, unique=True, index=True)
    secret_id = Column(Integer, default=random_remix_secret_id, unique=True, index=True)

    remix_original_song = relationship("OriginalSong", back_populates="remixes")
    # Put here with the hope it'd make generating questions easier
    # I'm not actually sure if it's doing that
    # question = relationship("Question", foreign_keys="[Question.correct_remix_id]")




class RemixArtist(Base):
    __tablename__ = "remix_artists"

    id = Column(Integer, primary_key=True, index=True)
    remix_artist_name = Column(String(600))
    remix_artist_ocremix_url = Column(String(600))

    remixes = relationship("Remix", backref="remix_artists")

class OriginalSong(Base):
    __tablename__ = "original_songs"

    id = Column(Integer, primary_key=True, index=True)
    original_song_title = Column(String(600), index=True)
    original_song_artist_id = Column(Integer, ForeignKey('original_artists.id'))
    original_song_videogame_id = Column(Integer, ForeignKey('videogames.id'))
    original_song_ocremix_url = Column(String(600), index=True)

    original_song_videogame = relationship("Videogame", back_populates="original_songs")

    remixes = relationship("Remix", back_populates="remix_original_song")

class OriginalArtist(Base):
    __tablename__ = 'original_artists'

    id = Column(Integer, primary_key=True, index=True)

    original_artist_name = Column(String(600), index=True)
    original_artist_ocremix_url = Column(String(600), index=True)

class Videogame(Base):
    __tablename__ = "videogames"

    id = Column(Integer, primary_key=True, index=True)
    videogame_title = Column(String(600), index=True)
    videogame_ocremix_url = Column(String(600), index=True)
    videogame_console = Column(String(600), index=True)

    original_songs = relationship("OriginalSong", back_populates="original_song_videogame")

# class Game(Base):
#     __tablename__ = "games"

#     id = Column(Integer, primary_key=True, index=True)
#     score  = Column(Integer)

#     questions = relationship("QuestionInstance", backref="games")

# class Question(Base):
#     __tablename__ = "questions"

#     id = Column(Integer, primary_key=True, index=True)
#     correct_remix_id = Column(Integer, ForeignKey('remixes.id'))
#     choice_1_remix_id = Column(Integer, ForeignKey('remixes.id'))
#     choice_2_remix_id = Column(Integer, ForeignKey('remixes.id'))
#     choice_3_remix_id = Column(Integer, ForeignKey('remixes.id'))

# class QuestionInstance(Base):
#     __tablename__ = "question_instances"

#     id = Column(Integer, primary_key=True, index=True)
#     question_id = Column(Integer, ForeignKey('questions.id'))
#     game_id = Column(Integer, ForeignKey('games.id'))
#     correct = Column(Boolean)
#     asked = Column(Boolean)

####################
# NON-DATABASE MODELS
####################

# Used in the post request to determine if the player chose the right answer
class Answer(BaseModel):
    secret_id: int
    public_id: int

class Choice(BaseModel):
    origin_game: str
    public_id: int

class Question(BaseModel):
    remix_youtube_url: str
    secret_id: int

class QuestionPackage(BaseModel):
    choices: List[Choice] = []
    question: Question
