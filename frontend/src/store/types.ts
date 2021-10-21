// export interface Answer {
//   secret_id: number,
//   public_id: number,
// }

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
