import { createStore } from 'vuex';
import { QuestionPackage, Choice } from './types';

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

  selectedAnswer: Choice | null = null;
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
  },
  mutations: {
    setQuestionPackage(state: State, payload) {
      state.questionPackage = payload;
    },
  },
  actions: {
    async getRemixes({ commit }) {
      const response = await fetch('/remixes/');
      const responseJson = await response.json();
      console.log(responseJson);
    },
    async submitRemixForParsing({ commit }, id: string) {
      const response = await fetch(`/parse/${id}`);
      const responseJson = await response.json();
      console.log(responseJson);
    },
    async getSong({ commit }) {
      const response = await fetch('/game/');
      const responseJson = await response.json();
      commit('setQuestionPackage', responseJson);
    },
    async seedDB() {
      const response = await fetch('/seed/');
      const responseJson = await response.json();
      console.log(responseJson);
    },
    async checkAnswer({ commit }, { public_id, secret_id }) {
      const response = await fetch('/game/', {
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
      console.log(responseJson);
    },
  },
  modules: {
  },
});
