import Vue from 'vue'
import App from './App.vue'
import {store} from './store'
import axios from 'axios'
import router from './router';

Vue.config.productionTip = false

Vue.prototype.$http = axios
Vue.prototype.$hostname = 'http://15.236.211.20:8000/api'
Vue.prototype.$domain = 'http://15.236.211.20:8080'

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app')
