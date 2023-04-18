from pydantic import BaseModel

class RemixBase(BaseModel):
    remix_youtube_url: str
    ocremix_remix_url: str
    remix_title: str

class RemixCreate(RemixBase):
    ocremix_remix_id: str
    pass

class Remix(RemixBase):
    id: int
    remix_artist_id: int
    remix_original_song_id: int

    class Config:
        orm_mode = True

class RemixArtistBase(BaseModel):
    remix_artist_name: str
    remix_artist_ocremix_url: str

class RemixArtistCreate(RemixArtistBase):
    pass

class RemixArtist(RemixArtistBase):
    id: int

    class Config:
        orm_mode = True

class OriginalSongBase(BaseModel):
    original_song_title: str
    original_song_ocremix_url: str

class OriginalSongCreate(OriginalSongBase):
    pass

class OriginalSong(OriginalSongBase):
    original_song_artist_id: int
    original_song_videogame_id: int

    class Config:
        orm_mode = True

class OriginalArtistBase(BaseModel):
    original_artist_name: str
    original_artist_ocremix_url: str

class OriginalArtistCreate(OriginalArtistBase):
    pass

class OriginalArtist(OriginalArtistBase):
    id: int

    class Config:
        orm_mode = True

class VideogameBase(BaseModel):
    videogame_title: str
    videogame_ocremix_url: str
    # videogame_console: str

class VideogameCreate(VideogameBase):
    pass

class Videogame(VideogameBase):
    id: int

    class Config:
        orm_mode = True

class GameBase(BaseModel):
    score: int

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    pass

class QuestionCreate(QuestionBase):
    correct_remix_id: int
    choice_1_remix_id: int
    choice_2_remix_id: int
    choice_3_remix_id: int

class Question(QuestionBase):

    class Config:
        orm_mode = True

class QuestionInstanceBase(BaseModel):
    pass;

class QuestionInstanceCreate(QuestionInstanceBase):
    question_id: int
    game_id: int
    correct: bool
    asked: bool

class Question(QuestionInstanceBase):
    id: int

    class Config:
        orm_mode = True
