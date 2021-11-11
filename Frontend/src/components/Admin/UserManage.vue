<!--
   Created on 2021/5/9 8:08 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div>

      <a-row style="margin: 0 0 30px 0" type="flex" align="middle">
        <!-------------------------- 搜索 --------------------------->
        <!-- <a-select  v-model="position" style="width: 120px; margin-right: 20px" @change="search" >
          <a-select-option value="all" >
            <a-icon type="rocket" class='position-icon'  style="margin-right: 8px;" />All
          </a-select-option>
          <a-select-option value="engineer" >
            <a-icon type="team" class='position-icon'/> Engineers
          </a-select-option>
          <a-select-option value="customer">
            <a-icon type="coffee" class='position-icon'/> Customers
          </a-select-option>
        </a-select> -->

        <a-input v-model="name" placeholder="用户名查询" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/>
        <a-input v-model="email" placeholder="邮箱查询" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/>

        <a-tooltip title="搜索">
          <a-button type="primary" shape="circle" icon="search" @click="search"  style="background: #8db2c3; border-color: #8db2c3; margin-right: 20px"/>
        </a-tooltip>
        <a-tooltip title="重置">
          <a-button type="primary" shape="circle" icon="delete" @click="refresh" style="background: #8db2c3; border-color: #8db2c3"/>
        </a-tooltip>

        <a-button type="primary" shape="round" style="margin-left:auto; right: 20px" @click="openEdit('Create')">添加用户</a-button>
      </a-row>
      <a-divider></a-divider>
      <UserEdit :visible="visible"
                :info="info"
                :mode="mode"
                :disabled="userEditEmailDisabled"
                @cancel="handleCancel"
                :confirmLoading="confirmLoading"
                @submit="handleSubmit" />
      <a-spin :spinning="loading">
      <a-table  :data-source="users" :pagination="false">


        <!-------------------------- 用户头像 姓名 性别--------------------------->
        <a-table-column title="姓名" key="name">
          <template slot-scope="row">
            <a-row type="flex" align="middle">
              <UserIcon :user="row" type="text"></UserIcon>
              <a-icon type="woman" v-if="row.gender==='female'" style="color: #ca53a1; margin-left: 5px"></a-icon>
              <a-icon type="man" v-else  style="color: #72909f; font-weight: bold; margin-left: 5px"></a-icon>
            </a-row>
          </template>
        </a-table-column>

        <!-------------------------- 邮箱 --------------------------->
        <a-table-column title="邮箱" key="email">
          <template slot-scope="row">
            {{ row.email}}
          </template>
        </a-table-column>

        <!-------------------------- 职务 --------------------------->
        <a-table-column title="所属部门" key="department">
          <template slot-scope="row" v-if="row.department_info.length">
            {{row.department_info[0].name}}
          </template>
        </a-table-column>

        <!-------------------------- 地区 --------------------------->
        <!-- <a-table-column title="Region" key="region">
          <template slot-scope="row">
            <span v-if="![null, undefined, ''].includes(row.region)">
             {{row.region}}
            </span>
            <span v-else>
              -
            </span>
          </template>
        </a-table-column> -->

        <!-------------------------- 是否为管理员 --------------------------->
        <a-table-column title="管理员权限" key="admin">
          <template slot-scope="row">
            <a-icon v-if='row.admin===true' type="check-circle" style="color: #3eca76"></a-icon>
            <a-icon  v-else type="close-circle" style="color: #dd4444" />
          </template>
        </a-table-column>

        <!-------------------------- 编辑 --------------------------->
        <a-table-column title="操作" key="action">
          <template slot-scope="row">
            <!-------------------------- 修改用户信息 --------------------------->
            <a-tooltip placement="top">
                <template slot="title">
                  <span>修改用户信息</span>
                </template>
              <a-icon type="edit" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="openEdit('Edit', row, true)" />
            </a-tooltip>

            <!-------------------------- 重置用户密码 --------------------------->
            <a-popconfirm
                title="确定要重置用户密码?  (重置为用户邮箱值)"
                ok-text="是"
                cancel-text="否"
                @confirm="resetPassword(row.id)"
                trigger="click"
            >
              <a-tooltip placement="top">
                <template slot="title">
                  <span>重置密码</span>
                </template>
                <a-icon type="thunderbolt" style="font-size: 20px; cursor:pointer; margin-right: 10px;" />
              </a-tooltip>
            </a-popconfirm>

            <!-------------------------- 详情 --------------------------->

            <a-tooltip placement="top">
              <template slot="title">
                <span>详情</span>
              </template>
              <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/profile/${row.id}`}).catch(e=>{console.log(e)})" />
            </a-tooltip>
          </template>
        </a-table-column>

      </a-table>
      </a-spin>
      <br><br>
      <a-pagination
          style="text-align: right"
          show-size-changer
          :total="count"
          :current="current"
          @change="onShowSizeChange"
          :page-size="page_size"
          @showSizeChange="onShowSizeChange"
      />
    </div>

</template>

<script>
import UserEdit from "@/components/Admin/UserEdit";
import UserService from "@/models/UserService";
import UserIcon from "@/components/Group/UserIcon";
export default {
    name: "UserManage",
    components:{UserIcon, UserEdit},

    data(){
        return{
          visible: false,
          confirmLoading: false,
          loading: false,
          mode: 'Create',
          default_info: {
            name: "",
            gender: "male",
            email: "",
            position: "engineer",
            admin: "false",
            region: "California, USA",
          },
          info:{},
          users: [],
          query: {},
          count: 0,
          current: 1,
          page_size: 10,
          position: 'all',
          name: '',
          email: '',
          userEditEmailDisabled: false,
        }
    },

    methods:{
      async onShowSizeChange(current, pageSize) {
        this.current = current
        this.page_size = pageSize
        await this.getUser()
      },

      /* 关闭create */
      handleCancel() {
        this.visible = false;
        this.confirmLoading = false;
      },

      /* 创建或者修改 */
      async handleSubmit(user_edit_form) {

        this.confirmLoading = true;
        try{
          if (this.mode === 'Create'){
            await UserService.create(user_edit_form)
          }
          else{
            user_edit_form['id'] = this.info['id']
            await UserService.update(user_edit_form)
          }
          setTimeout(() => {
            /* 延迟关闭表单 */
            this.getUser()
            this.$message.success(this.mode === 'Create'? '创建成功！': '修改成功！')
            this.visible = false;
            this.confirmLoading = false;
            this.handleCancel()
          }, 2000);
        }catch{
          this.visible = false
          this.handleCancel()
          return
        }
      },

      /* 打开create 表单 */
      openEdit(mode, info=undefined, emailDisabled=false){
        this.mode=mode
        if(this.mode === 'Edit'){
          info.admin = info.admin ? 'true': 'false'
          this.info = info
        }
        else{
          this.info = this.default_info
        }
        this.visible=true
        this.userEditEmailDisabled = emailDisabled
      },

      /* 搜索 */
      async search(){
        this.query = {}
        if(this.position !== 'all'){
          this.query['position'] = this.position
        }
        if(this.name !== ''){
          this.query['name'] = {"$regex": this.name}
        }
        if(this.email !== ""){
          this.query['email'] = {"$regex": this.email}
        }
        this.current = 1
        await this.getUser()
      },

      /* 重置搜索，页面等 */
      async refresh(){
        this.position = 'all'
        this.name = ""
        this.email = ""
        await this.search()
      },

      async getUser(){
        this.loading = true
        try{
          let index = 0
          let res = await UserService.find({
            filter: this.query,
            limit: this.page_size,
            skip: (this.current-1)*this.page_size
          })
          this.count = res['count']
          let users = res['results']
          users.forEach(e=>{
            e.key=index
            index += 1
          })
          this.users = users

        }finally {
          this.loading = false
        }
      },

      /* 重置密码 */
      async resetPassword(user_id){
        await UserService.resetPassword(user_id)
        this.$message.success('Reset successfully!')
      }
    },

    mounted(){
      this.getUser()
    },
}
</script>

<style scoped>
>>> .ant-btn{
  font-weight: bold;
}

.position-icon{
  font-weight: bold;
  font-size: 110%;
  margin-right: 5px;
}

</style>
