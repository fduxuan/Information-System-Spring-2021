<!--
   Created on 2021/5/9 7:05 下午

   @Author: fduxuan

   Desc: admin页面，添加用户，用户等级管理
 */
 -->
<template>
  <div style="padding: 20px 20px 40px 20px;">
    <a-card class="card-content">
      <a-tabs v-if="$store.state.user.admin">
        <a-tab-pane key="1" tab="用户管理">
          <UserManage></UserManage>
        </a-tab-pane>
        <a-tab-pane key="2" tab="部门管理">
          <DepartmentManage></DepartmentManage>
        </a-tab-pane>
<!--        <a-tab-pane key="2" tab="User Relations">-->
<!--          <UserRelation></UserRelation>-->
<!--        </a-tab-pane>-->
<!--        <a-tab-pane key="3" tab="Records">Content of Tab Pane 2</a-tab-pane>-->
      </a-tabs>
      <a-result v-else status="500" title="抱歉, 您没有访问此页面的权限" sub-title="请联系管理员">
        <template #extra>
          <a-button type="primary" style="font-weight: bold" @click="$router.push({ path:'/'}).catch(e=>{console.log(e)})">
            返回主页
          </a-button>
        </template>
      </a-result>
    </a-card>
  </div>

</template>

<script>
import UserManage from "@/components/Admin/UserManage";
import DepartmentManage from "@/components/Admin/DepartmentManage";
export default {
    name: "Admin",
    components:{
      UserManage,
      DepartmentManage
    },
    data(){
        return{}
    },

    methods:{

    },

    mounted(){

    },
}
</script>

<style scoped>
>>>.ant-tabs-nav .ant-tabs-tab{
  font-weight: bold;
}

.card-content{
  text-align: left;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  box-shadow:-1px 1px 3px #ACADA3;
}
>>> .ant-tabs .ant-tabs-top-content > .ant-tabs-tabpane, .ant-tabs .ant-tabs-bottom-content > .ant-tabs-tabpane{
  padding: 0 20px 10px 10px
}
</style>
