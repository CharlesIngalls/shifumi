import Vue from 'vue';
import VueRouter from 'vue-router';

import HelloWorld from './components/HelloWorld'
import Game from './components/Game'

Vue.use(VueRouter);

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: HelloWorld,
        },
        {
            path: '/:access_id',
            component: Game,
        },
    ],
});
