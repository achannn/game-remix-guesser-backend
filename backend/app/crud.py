from sqlalchemy.orm import Session

from . import models, schemas, internal

# REMIX
def get_remix(db: Session, remix_id: int):
    return db.query(models.Remix).filter(models.Remix.id == remix_id).first()

def get_remixes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Remix).offset(skip).limit(limit).all()

def get_remix_by_title(db: Session, remix_title: str):
    return db.query(models.Remix).filter_by(remix_title=remix_title)

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

def deep_create_remix(
        db: Session,
        remix: schemas.RemixCreate,
        remix_artist: schemas.RemixArtistCreate,
        remix_original_song: schemas.OriginalSongCreate,
        original_artist: schemas.OriginalArtistCreate,
        videogame: schemas.VideogameCreate):

    remix_artist_db = get_remix_artist_by_name(db, remix_artist['remix_artist_name'])

    if remix_artist_db is None:
        remix_artist_db = create_remix_artist(db, remix_artist)

    remix_original_song_db = get_original_song_by_title(db, original_song_title=remix_original_song['original_song_title'][0])
    print("what was the result of get original song function?")
    print(remix_original_song_db)

    if remix_original_song_db is None:
        remix_original_song_db = deep_create_original_song(db, remix_original_song, original_artist, videogame)

    return create_remix(db, remix, remix_artist_db['id'], remix_original_song_db['id'])


# REMIX ARTIST

def get_remix_artist(db: Session, remix_artist_id: int):
    return db.query(models.RemixArtist).filter(models.RemixArtist.id == remix_artist_id).first()

def get_remix_artist_by_name(db: Session, remix_artist_name: str):
    query = db.query(models.RemixArtist).filter_by(remix_artist_name=remix_artist_name).first()
    print("remix artist by name query inc")
    print(query)
    return query

def create_remix_artist(db: Session, remix_artist: schemas.RemixArtistCreate):
    db_remix_artist = models.RemixArtist(**remix_artist)
    db.add(db_remix_artist)
    db.commit()
    db.refresh(db_remix_artist)
    return db_remix_artist

# ORIGINAL SONG

def get_original_song(db: Session, original_song_id: int):
    return db.query(models.OriginalSong).filter(models.OriginalSong.id == original_song_id).first()

def get_original_song_by_title(db: Session, original_song_title: str):
    print("are we getting the right stuff?")
    print(original_song_title)

    query = db.query(models.OriginalSong).filter_by(original_song_title=original_song_title)
    print(query.all())

    return db.query(models.OriginalSong).filter_by(original_song_title=original_song_title).first()

def create_original_song(db: Session, original_song: schemas.OriginalSongCreate, original_song_artist_id, original_song_videogame_id):
    db_original_song = models.OriginalSong(
        **original_song,
        original_song_artist_id=original_song_artist_id,
        original_song_videogame_id=original_song_videogame_id
        )
    db.add(db_original_song)
    db.commit()
    db.refresh(db_original_song)
    return db_original_song

def deep_create_original_song(db: Session, original_song: schemas.OriginalSongCreate, original_artist_create: schemas.OriginalArtistCreate, videogame_create: schemas.VideogameCreate):

    original_artist_db = get_original_artist_by_name(db, original_artist_create['original_artist_name'])

    if (original_artist_db is None):
        # Make song
        original_artist_db = create_original_artist(db, original_artist_create)

    print("what is videogame create?")
    videogame_db = get_videogame_by_title(db, videogame_create['title'])

    if (videogame_db is None):
        videogame_db = create_videogame(db, videogame_create)

    return create_original_song(db, original_song, original_artist_db.id, videogame_db.id)

def get_original_artist(db: Session, original_artist_id: int):
    return db.query(models.OriginalArtist).filter(models.OriginalArtist.id == original_artist_id).first()

def create_original_artist(db: Session, original_artist: schemas.OriginalArtistCreate):
    db_original_artist = models.OriginalArtist(**original_artist)
    db.add(db_original_artist)
    db.commit()
    db.refresh(db_original_artist)
    return db_original_artist

def get_original_artist_by_name(db: Session, original_artist_name: str):
    return db.query(models.OriginalArtist).filter_by(original_artist_name=original_artist_name).first()

# VIDEOGAME

def get_videogame(db: Session, videogame_id: int):
    return db.query(models.Videogame).filter(models.Videogame.id == videogame_id).first()

def get_videogame_by_title(db: Session, videogame_title):
    return db.query(models.Videogame).filter_by(videogame_title=videogame_title).first()

def create_videogame(db: Session, videogame: schemas.VideogameCreate):
    db_videogame = models.Videogame(**videogame)
    db.add(db_videogame)
    db.commit()
    db.refresh(db_videogame)
    return db_videogame
