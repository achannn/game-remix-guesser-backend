export interface CorrectAnswer {
  origin_game: string,
  remix_artist: string,
  ocremix_remix_url: string,
  original_song_title: string,
}

export interface Choice {
  origin_game: string,
  public_id: number,
}

export interface Question {
  remix_youtube_url: string,
  secret_id: number,
}

export interface QuestionPackage {
  choices: Choice[],
  question: Question,
}
