<!--
   Created on 2021/5/26 1:47 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
  <div style="padding: 20px 20px 40px 20px;">
    <a-card class="card-content">
      <h1> 部门信息</h1>
      <a-divider></a-divider>
      <a-row>
        <a-col :span="6">
          <a-card >
            <img
                style="width: 100%"
                alt="/"
                src="https://minio.droproblem.com/avatar2/logo_black.png"
            />
            <br><br>
            <!----------------------- 姓名/邮箱/职位 ---------------------->
            <a-card-meta>

              <template slot="description">
                <a-row style="font-size: 110%; font-weight: bold; color: #000;" type="flex" align="middle" justify="center">
                  {{department.name}}
                </a-row>
                <a-divider style="margin-bottom: 10px"></a-divider>
                <a-row type="flex" align="middle"><a-icon type="mail" style="margin-right: 20px; color:#000"/>{{department.leader}}</a-row>
                <a-divider style="margin: 10px 0 10px 0"></a-divider>
                <a-row type="flex" align="middle" ><a-icon type="flag" style="margin-right: 20px; color:#000"/>{{leader.name}}</a-row>
              </template>
            </a-card-meta>
          </a-card>
        </a-col>
        <a-col :span="17" :offset="1">
          <DepartmentUserManage :did=did></DepartmentUserManage>
        </a-col>
      </a-row>
    </a-card>
  </div>

</template>

<script>
import UserService from "@/models/UserService";
import DepartmentService from "@/models/DepartmentService";
import DepartmentUserManage from "@/components/Admin/DepartmentUserManage";
export default {
    name: "UserProfile",
    components:{
        DepartmentUserManage
    },
    data(){
        return{
          did: "",
          leader: {
            name: ""
          },
          department: {
            name: "",
            leader: ""
          },
          loading: false,
        }
    },
    props: {
    },

    methods:{

      /* 获取个人信息 或者其他人信息 */
      async info(){
        this.department = await DepartmentService.show(this.did);
        if (this.department.leader) {
          let leader = await UserService.find({filter: {email: this.department.leader}});
          this.leader = leader.results[0];
        }
      }
    },

    async mounted(){
      this.did = this.$route.params.did
      await this.info()
    },

    watch: {
      async '$route' (to, from) { //监听路由是否变化
        if(to.params.did !== from.params.did){
          this.did = to.params.did;
          await this.info()
        }
      }
    },

}
</script>

<style scoped>
.card-content{
  text-align: left;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  box-shadow:-1px 1px 3px #ACADA3;
}

/* >>> .anticon{
  margin-right: 20px; color:#000
} */

>>>.ant-upload.ant-upload-select{
  display: block;
  cursor: pointer;
}

</style>
