import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

import VueSocketio from 'vue-socket.io-extended';
import io from 'socket.io-client';

// for local development...
//Vue.use(VueSocketio, io('http://192.168.2.2:8899'), { store });

Vue.use(VueSocketio, io(), { store });

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
