import { createStore } from 'vuex';

export default createStore({
  state: {
    currentRemixUrl: '',
  },
  mutations: {
    setCurrentRemixUrl(state, payload) {
      state.currentRemixUrl = payload;
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
    async generateQuestion() {
      const response = await fetch('/game/');
      const responseJson = await response.json();
      console.log(responseJson);
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
