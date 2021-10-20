from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base



class Remix(Base):
    __tablename__ = "remixes"

    id = Column(Integer, primary_key=True, index=True)
    ocremix_remix_id = Column(String(20), index=True)
    remix_youtube_url = Column(String(600), index=True)
    ocremix_remix_url = Column(String(600), index=True)
    remix_title = Column(String(600), index=True)
    remix_artist_id = Column(ForeignKey('remix_artists.id'))
    remix_original_song_id = Column(ForeignKey('original_songs.id'))

    # Put here with the hope it'd make generating questions easier
    # I'm not actually sure if it's doing that
    question = relationship("Question", foreign_keys="[Question.correct_remix_id]")


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

    remixes = relationship("Remix", backref="original_songs")

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

    original_songs = relationship("OriginalSong", backref="videogames")

# class Game(Base):
#     __tablename__ = "games"

#     id = Column(Integer, primary_key=True, index=True)
#     score  = Column(Integer)

#     questions = relationship("QuestionInstance", backref="games")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    correct_remix_id = Column(Integer, ForeignKey('remixes.id'))
    choice_1_remix_id = Column(Integer, ForeignKey('remixes.id'))
    choice_2_remix_id = Column(Integer, ForeignKey('remixes.id'))
    choice_3_remix_id = Column(Integer, ForeignKey('remixes.id'))

# class QuestionInstance(Base):
#     __tablename__ = "question_instances"

#     id = Column(Integer, primary_key=True, index=True)
#     question_id = Column(Integer, ForeignKey('questions.id'))
#     game_id = Column(Integer, ForeignKey('games.id'))
#     correct = Column(Boolean)
#     asked = Column(Boolean)
