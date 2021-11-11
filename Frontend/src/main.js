import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.less'
import './assets/style/group.css'
import VueCropper from 'vue-cropper'
import vueKanban from 'vue-kanban'

import 'vue-kanban/src/assets/kanban.css'

Vue.use(vueKanban)

// 引入v-chart 图表
import VCharts from 'v-charts'
Vue.use(VCharts)

Vue.use(VueCropper)

Vue.config.productionTip = false;

Vue.use(Antd);

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
