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
      const response = await fetch('/game/');
      const responseJson = await response.json();
      console.log(responseJson);
    },
  },
  modules: {
  },
});
