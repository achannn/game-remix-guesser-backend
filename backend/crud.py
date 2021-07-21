from sqlalchemy.orm import Session

from . import models, schemas

# REMIX
def get_remix(db: Session, remix_id: int):
    return db.query(models.Remix).filter(models.Remix.id == remix_id).first()

def get_remixes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Remix).offset(skip).limit(limit).all()

def create_remix(db: Session, remix: schemas.RemixCreate, remix_artist_id: int, remix_original_song_id: int):
    db_remix = models.Remix(
        **remix.Dict(),
        remix_artist_id=remix_artist_id,
        remix_original_song_id=remix_original_song_id
    )
    db.add(db_remix)
    db.commit()
    db.refresh(db_remix)
    return db_remix

# REMIX ARTIST

def get_remix_artist(db: Session, remix_artist_id: int):
    return db.query(models.RemixArtist).filter(models.RemixArtist.id == remix_artist_id).first()

def create_remix_artist(db: Session, remix_artist: schemas.RemixArtistCreate):
    db_remix_artist = models.RemixArtist(**remix_artist.dict())
    db.add(db_remix_artist)
    db.commit()
    db.refresh(db_remix_artist)
    return db_remix_artist

# ORIGINAL SONG

def get_original_song(db: Session, original_song_id: int):
    return db.query(models.OriginalSong).filter(models.OriginalSong.id == original_song_id).first()

def create_original_song(db: Session, original_song: schemas.OriginalSongCreate, original_song_artist_id, original_song_videogame_id):
    db_original_song = models.OriginalSong(
        **original_song.dict,
        original_song_artist_id=original_song_artist_id,
        original_song_videogame_id=original_song_videogame_id
        )
    db.add(db_original_song)
    db.commit()
    db.refresh(db_original_song)
    return db_original_song

# ORIGINAL ARTIST

def get_original_artist(db: Session, original_artist_id: int):
    return db.query(models.OriginalArtist).filter(models.OriginalArtist.id == original_artist_id).first()

def create_original_artist(db: Session, original_artist: schemas.OriginalArtistCreate):
    db_original_artist = models.OriginalArtist(**original_artist.dict)
    db.add(db_original_artist)
    db.commit()
    db.refresh(db_original_artist)
    return db_original_artist

# VIDEOGAME

def get_videogame(db: Session, videogame_id: int):
    return db.query(models.Videogame).filter(models.Videogame.id == videogame_id).first()

def create_videogame(db: Session, videogame: schemas.VideogameCreate):
    db_videogame = models.Videogame(**videogame.dict)
    db.add(db_videogame)
    db.commit()
    db.refresh(db_videogame)
    return db_videogame
