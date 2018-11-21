import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const votes = {
  state: {
    votes: {},
    isConnected: false,
  },
  mutations: {
    SOCKET_CONNECT(state, status) {
      //console.log("Connect: " + status);
      state.isConnected = true;
    },
    SOCKET_REGISTER(state, data) {
      //console.log("id: " + data['id'] + " name: " + data['name']);
      let name = data['name'];
      let id = data['id'];
      if(state.votes[id] === undefined) {
        Vue.set(state.votes,id,{ name, votes: [] });
      } else {
        Vue.set(state.votes[id],'name',name);
      }
    },
    SOCKET_VOTE(state, data) {
      let id = data['id'];
      let number = data['number'];
      let value = data['value'];
      //console.log("id: " + id + " number: " + number + " value: " + value);
      if(state.votes[id] === undefined) {
        Vue.set(state.votes,id,{ 'name': "Unknown", votes: [] });
      }
      Vue.set(state.votes[id]['votes'],parseInt(number),parseInt(value));
    }
  }
};

export default new Vuex.Store({
  modules: {
    votes,
  }
})