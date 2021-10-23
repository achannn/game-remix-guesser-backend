import { createStore } from 'vuex';
import { QuestionPackage, Choice, CorrectAnswer } from './types';
import { fetchApi } from './fetch';

// In which I question whether typescript is really worth the headache
// ts-ignore
function getYoutubeIdFromUrl(url: any) {
  // eslint-disable-next-line
  // ts-ignore
  const blah = url.split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
  // ts-ignore
  // eslint-disable-next-line
  return (blah[2] !== undefined) ? blah[2].split(/[^0-9a-z_\-]/i)[0] : blah[0];
}

export class State {
  questionPackage: QuestionPackage | null = null;

  selectedAnswer: number | null = null;

  correctAnswer: CorrectAnswer | null = null;

  hasCheckedAnswer = false;
}

// export interface StateInterface extends State {};

export default createStore({
  state: new State(),
  getters: {
    currentQuestionYoutubeId: (state: State): string | null => {
      if (state.questionPackage?.question?.remix_youtube_url) {
        return getYoutubeIdFromUrl(state.questionPackage.question.remix_youtube_url);
      }
      return null;
    },
    currentQuestionChoices: (state: State): Choice[] | null => {
      if (state.questionPackage?.choices?.length) {
        return state.questionPackage.choices;
      }
      return null;
    },
    correctAnswer: (state: State): CorrectAnswer | null => state.correctAnswer,
    hasCheckedAnswer: (state: State): boolean => state.hasCheckedAnswer,
  },
  mutations: {
    setQuestionPackage(state: State, payload) {
      state.questionPackage = payload;
    },
    setSelectedChoice(state: State, choice: number) {
      state.selectedAnswer = choice;
    },
    clearGameState(state: State) {
      state.selectedAnswer = null;
      state.correctAnswer = null;
      state.questionPackage = null;
      state.hasCheckedAnswer = false;
    },
    setCorrectAnswer(state: State, answer: CorrectAnswer) {
      state.correctAnswer = answer;
    },
    setHasCheckedAnswer(state: State, hasChecked: boolean) {
      state.hasCheckedAnswer = hasChecked;
    },
  },
  actions: {
    async getRemixes() {
      const response = await fetchApi('/remixes/');
      const responseJson = await response.json();
      console.log(responseJson);
    },
    // Lol how do you do no first argument to an action in vuex
    // without angering the linter or typescript?
    // eslint-disable-next-line
    async submitRemixForParsing({}, id: string) {
      const response = await fetchApi(`/parse/${id}`);
      const responseJson = await response.json();
      console.log(responseJson);
    },
    async getSong({ commit }) {
      commit('clearGameState');
      const response = await fetchApi('/game/');
      const responseJson = await response.json();
      commit('setQuestionPackage', responseJson);
    },
    async seedDB() {
      const response = await fetchApi('/seed/');
      const responseJson = await response.json();
      console.log(responseJson);
    },
    async submitAnswer({ state, commit }) {
      commit('setHasCheckedAnswer', false);
      const secret_id = state.questionPackage?.question.secret_id;
      const public_id = state.selectedAnswer;
      const response = await fetchApi('/game/', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          public_id,
          secret_id,
        }),
      });
      const responseJson = await response.json();
      commit('setCorrectAnswer', responseJson);
      commit('setHasCheckedAnswer', true);
    },
  },
  modules: {
  },
});
