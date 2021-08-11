import Vue from "vue";
import VueCookies from 'vue-cookies'
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueApexCharts from "vue-apexcharts";
import VueDraggableResizable from "vue-draggable-resizable";
import "vue-draggable-resizable/dist/VueDraggableResizable.css";

const server = 'http://localhost:5000';
console.log(server);
Vue.component('vue-draggable-resizable', VueDraggableResizable);
Vue.component('apexchart', VueApexCharts);
Vue.use(VueCookies)
Vue.config.productionTip = false;
Vue.$cookies.config('7d')

new Vue({
        router,
        store,
        vuetify,
        render: h => h(App)
    })
    .$mount("#app");