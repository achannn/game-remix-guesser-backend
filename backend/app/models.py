from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base



class Remix(Base):
    __tablename__ = "remixes"

    id = Column(Integer, primary_key=True, index=True)
    remix_youtube_url = Column(String, index=True)
    ocremix_remix_url = Column(String, index=True)
    remix_title = Column(String, index=True)
    remix_artist_id = Column(ForeignKey('RemixArtist.id'))
    remix_original_song_id = Column(ForeignKey('OriginalSong.id'))


class RemixArtist(Base):
    __tablename__ = "remix_artists"

    id = Column(Integer, primary_key=True, index=True)
    remix_artist_name = Column(String)
    remix_artist_ocremix_url = Column(String)

    remixes = relationship("Remix", backref="remix_artists")

class OriginalSong(Base):
    __tablename__ = "original_songs"

    id = Column(Integer, primary_key=True, index=True)
    original_song_title = Column(String, index=True)
    original_song_artist_id = Column(Integer, ForeignKey('original_artists.id'))
    original_song_videogame_id = Column(Integer, ForeignKey('videogames.id'))
    original_song_ocremix_url = Column(String, index=True)


class OriginalArtist(Base):
    __tablename__ = 'original_artists'

    id = Column(Integer, primary_key=True, index=True)

    original_artist_name = Column(String, index=True)
    original_artist_ocremix_url = Column(String, index=True)

class Videogame(Base):
    __tablename__ = "videogames"

    id = Column(Integer, primary_key=True, index=True)
    videogame_title = Column(String, index=True)
    videogame_ocremix_url = Column(String, index=True)
    videogame_console = Column(String, index=True)

    original_songs = relationship(OriginalSong, backref="videogames")
