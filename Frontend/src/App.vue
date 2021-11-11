<template>
  <a-config-provider :locale="locale">
  <div id="app">

    <Header></Header>
    <Transition   v-if="spinning"></Transition>
    <router-view v-else-if="this.$store.state.user!==null" />
    <Home v-else></Home>

    <a-back-top :visibilityHeight="100">
      <div class="ant-back-top-inner">
        <a-icon type="up" />
      </div>
    </a-back-top>

  </div>
  </a-config-provider>
</template>


<script>
import Transition from "@/components/Group/Transition";
import Home from "@/views/Home";
import UserService from "@/models/UserService";
import Header from "./components/Group/Header.vue"
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN';
export default {
  name: 'APP',
  components: {
    Header, Transition, Home
  },
  data(){
    return{
      spinning: false,
      locale: zhCN,
    }
  },

  mounted() {
    this.spinning = true
    UserService.info().then(u=>{
      this.$store.commit('set_user', u)
    }).catch(e=>{
      this.$store.commit('set_user', null)
      console.log(e)
    }).finally(()=>{
      this.spinning = false
    })
  }
}
</script>


<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: #eeeeee;
  height: 100%;
  min-width: 1200px;
}

/* #app .ant-back-top {
  bottom: 40px;
} */

#app .ant-back-top-inner {
  height: 50px;
  width: 50px;
  line-height: 48px;
  border-radius: 50%;
  text-align: center;
  font-size: 20px;
  background-color: rgb(141, 178, 195);
  color: white;
  transition: box-shadow .3s;
}

#app .ant-back-top-inner:hover {
  box-shadow: 0 10px 15px 0 rgb(0 0 0 / 10%);
  -webkit-box-shadow: 0 10px 15px 0 rgb(0 0 0 / 10%);
}

</style>
