<template>
  <div class="home">
    <div style="position: absolute; top: 20%; right: 10%; text-align: center">
      <span style="font-size: 300%;font-style: italic">项目管理</span>
      <span style="font-size: 150%;font-style: italic;color: #d19c9c; margin-left: 5px">信息系统设计2021</span>

      <br><br>
      <div class="login-form" v-if="this.$store.state.user === null">
        <a-form-model :model="user_login">
          <!----------------------- 邮箱 ---------------------->
          <a-form-model-item>
            <a-row>
              <a-col :span="4" ><span>邮箱:</span></a-col>
              <a-col :span="16" style="text-align: right">
                <a-input class="login-input" v-model="user_login.email" size="large"></a-input>
              </a-col>
            </a-row>

          </a-form-model-item>
          <br>

          <!----------------------- 密码 ---------------------->
          <a-form-model-item>
            <a-row>
              <a-col :span="4" ><span>密码:</span></a-col>
              <a-col :span="16">
                <a-input class="login-input" type="password"  v-model="user_login.password" size="large"></a-input>
              </a-col>
            </a-row>
          </a-form-model-item>
        </a-form-model>

        <a-row style="text-align: right; margin-right: 30px">
          <a-button  ghost @click="login">登录</a-button>
        </a-row>
      </div>

      <div class="login-form" v-else>
        <br>
        <span style="font-size: 200%; ">您好！ {{this.$store.state.user.name}}</span>

        <br><br><br>
        <span style="font-size: 200%;color:#9cced1;">{{current_time}}</span>

      </div>

    </div>


  </div>
</template>

<script>

import UserService from "@/models/UserService";
import moment from "moment";
export default {
  name: 'Home',
  components: {

  },

  data(){
    return{
      user_login: {
        email: "",
        password: ""
      },
      current_time: ""
    }
  },

  methods:{
    async login(){
      await UserService.login(this.user_login)
      let user = await UserService.info()
      this.$store.commit('set_user', user)
    },

    getToday(){
      // let date = new Date()
      moment.locale('zh-cn');
      this.current_time = moment().format('MM/DD YYYY HH:mm ddd')
      console.log(this.current_time)
    }
  },

  async mounted() {
    this.getToday()
  }
}
</script>

<style scoped>
.home{
  background: url("../assets/backgroud.png") rgba(0, 0, 0, 0.2) no-repeat center center;
  background-blend-mode: multiply;
  height: calc(100% - 55px);
  width: 100%;
  background-size:cover
}

span{
  font-weight: bold;
  color: #fff;
  font-size: 120%;
}

.login-form{
  border: 3px solid #eeeeee;
  padding: 40px 20px 20px 20px;
  border-radius: 5px;
}
.login-input{
  width: 300px;
  margin: 0 20px;
  background: none;
  color: #d1e0d5;
  font-weight: bolder;
  border-width: 2px;
}

>>> .ant-btn{
  border-width: 2px;
  font-weight: bold;
}
</style>
