<!--
   Created on 2021/4/4 5:44 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
  <div class="header-content" >
    <!----------------------- logo和标题 项目管理 ----------------------->
    <img src="../../assets/logo.png" style='padding:0 18px 0 18px; height: 35px; color: #fff' alt="" />
    <span style="font-size: 180%; font-style: italic; cursor: pointer; margin-right: 5px"
          @click="goRoute('')">
      项目管理
    </span>
    <span style="font-size: 120%; color: #d19c9c; font-style: italic; margin-right: 30px;cursor: pointer"
          @click="goRoute('')">
      信息系统设计2021
    </span>

    <!----------------------- 导航栏 ----------------------->

    <a-button v-if="this.$store.state.user!==null" class="header-nav" ghost type="primary" shape="round" @click="goRoute('project')">项目列表</a-button>

    <a-button v-if="this.$store.state.user!=null&&this.$store.state.user.username!=='admin'" class="header-nav" ghost type="primary" shape="round" @click="goRoute('notification')">通知列表</a-button>

    <a-button v-if="$store.state.user && $store.state.user.admin" class="header-nav" ghost type="primary" shape="round" @click="goRoute('admin')">系统管理</a-button>

    <a-button  class="header-nav" ghost type="primary" shape="round" href="http://106.14.244.24:8080/docs/">关于我们</a-button>


    <!----------------------- 个人信息 ----------------------->
    <a-dropdown v-if="this.$store.state.user!==null">
      <a-row type="flex" align="middle" class="user-info">
        <a-avatar :src="$store.state.user.avatar"  />
        <span style="font-size: 120%; font-weight: bold; margin-left:15px">{{ this.$store.state.user.name }}</span>
      </a-row>
      <a-menu slot="overlay" class="user-info-nav">
        <!----------------------- 个人资料 ----------------------->
        <a-menu-item @click="goRoute(`profile/${$store.state.user.id}`)">
          <a-icon type="user" style="font-size: 110%; font-weight: bold"/><span>个人信息</span>
        </a-menu-item>
        <!----------------------- 退出登录 ----------------------->
        <a-menu-item>
          <a-icon @click="logout" type="logout" style="font-size: 110%; font-weight: bold" /><span @click="logout" >退出登录</span>
        </a-menu-item>
      </a-menu>
    </a-dropdown>

  </div>

</template>

<script>
import UserService from "@/models/UserService";
export default {
    name: "Header",
    components:{

    },
    data(){
        return{}
    },

    methods:{
      goRoute(path){
        this.$router.push({ path:'/'+path}).catch(e=>{console.log(e)})
      },

      async logout(){
        await UserService.logout()
        this.$store.commit('set_user', null)
      }
    },

    mounted(){

    },
}
</script>

<style scoped>
.header-content{
  height: 55px;
  background: #222831;
  color: #eaeaea;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.header-nav{
  margin: 0 20px;
  font-weight: bold;
}
>>> .ant-btn.ant-btn-primary.ant-btn-round.ant-btn-background-ghost{
  color: #9cd1d0;
  border-color: #9cd1d0
}

/* 圆角focus变手 */
.user-info{
  margin-left: auto;
  margin-right: 20px;
  padding: 4px 8px 4px 8px;
  border-radius: 10px;
  cursor: pointer;
}
.user-info:hover{
  background: #424b51;
}

.user-info-nav{
  background: #424b51;
  color: #eaeaea;
  margin: 3px 0 5px 0;
  padding: 1px 0 1px 0;
  border-radius: 3px;
}

>>>.ant-dropdown-menu-item{
  color: #eaeaea;
  align-items: center;
}

>>>.ant-dropdown-menu-item:hover {
  color: #000;
}

span{
  font-weight: bold;
}
</style>
