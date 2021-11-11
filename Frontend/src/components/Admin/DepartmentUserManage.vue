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

        <a-input v-model="name" placeholder="用户姓名筛选" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/>
        <a-input v-model="email" placeholder="用户邮箱筛选" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/>

        <a-tooltip title="Search">
          <a-button type="primary" shape="circle" icon="search" @click="search"  style="background: #8db2c3; border-color: #8db2c3; margin-right: 20px"/>
        </a-tooltip>
        <a-tooltip title="Clear">
          <a-button type="primary" shape="circle" icon="delete" @click="refresh" style="background: #8db2c3; border-color: #8db2c3"/>
        </a-tooltip>

        <!-- <a-button type="primary" shape="round" style="margin-left:auto; right: 20px" @click="openEdit('Create')">New User</a-button> -->
        <a-button type="primary" shape="round" style="margin-left:auto; right: 20px" @click="openInvite()">邀请用户</a-button>
      </a-row>
      <a-divider></a-divider>
      <a-modal v-model="is_invite_visible" title="邀请用户"
               @cancel="handleInviteCancel"
               @ok="handleInviteOk"
               :confirm-loading="confirmInviteLoading"
               :key="stamp"
               >
        <a-form-model :model="user_invite" ref="user_invite_form" :rules="user_invite_rules">
          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 邮箱 ---------------------->
            <a-form-model-item label="邀请公司用户" prop="email">
              <UserSelect @change="(e)=>{user_invite.email=e.email}"></UserSelect>
            </a-form-model-item>
          </a-row>
        </a-form-model>
      </a-modal>
      <UserEdit :visible="visible"
                :info="info"
                :mode="mode"
                @cancel="handleCancel"
                :confirmLoading="confirmLoading"
                @submit="handleSubmit">

      </UserEdit>
      <a-spin :spinning="loading">
      <a-table  :data-source="users" :pagination="false">


        <!-------------------------- 用户头像 姓名 性别--------------------------->
        <a-table-column title="姓名" key="name">
          <template slot-scope="row">
            <a-row type="flex" align="middle">
              <UserIcon :user="row" type="text" style="margin-right: 5px"></UserIcon>
              <a-icon type="woman" v-if="row.gender==='female'" style="color: #ca53a1"></a-icon>
              <a-icon type="man" v-else  style="color: #72909f; font-weight: bold"></a-icon>
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
        <!-- <a-table-column title="Department" key="department">
          <template slot-scope="row" v-if="row.department_info.length">
            {{row.department_info[0].name}}
          </template>
        </a-table-column> -->

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
            <!-- <a-tooltip placement="top">
                <template slot="title">
                  <span>Edit Information</span>
                </template>
              <a-icon type="edit" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="openEdit('Edit', row)" />
            </a-tooltip> -->

            <!-------------------------- 重置用户密码 --------------------------->
            <!-- <a-popconfirm
                title="Are you sure to reset this user's password?  (Reset to email value )"
                ok-text="Yes"
                cancel-text="No"
                @confirm="resetPassword(row.id)"
                trigger="click"
            >
              <a-tooltip placement="top">
                <template slot="title">
                  <span>reset password</span>
                </template>
                <a-icon type="thunderbolt" style="font-size: 20px; cursor:pointer; margin-right: 10px;" />
              </a-tooltip>
            </a-popconfirm> -->

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
import DepartmentService from "@/models/DepartmentService";
import UserSelect from "@/components/Admin/UserSelect";
import UserIcon from "@/components/Group/UserIcon";
export default {
    name: "DepartmentUserManage",
    components:{UserIcon, UserEdit, UserSelect},
    props: {
      did: {
        type: String,
        default() { return ""; }
      }
    },

    data(){
        return{
          id: "",

          is_invite_visible: false,
          confirmInviteLoading: false,
          default_user_invite: {
            email: ""
          },
          user_invite: {
            email: ""
          },
          user_invite_rules: {
            email:[{ required: true, message: "邮箱不可为空", trigger: 'blur' }],
          },

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
          stamp: '123'
        }
    },

    methods:{
      /* 关闭create */
      handleInviteCancel() {
        this.is_invite_visible = false;
        this.confirmInviteLoading = false;
      },

      /* 创建或者修改 */
      async handleInviteOk() {
        try{
          await this.$refs.user_invite_form.validate();
          this.confirmInviteLoading = true;
          await DepartmentService.invite(this.id, this.user_invite.email);
          setTimeout(() => {
            /* 延迟关闭表单 */
            this.getUser()
            this.$message.success('成功邀请加入部门！')
            this.handleInviteCancel()
          }, 2000);
        }catch{
          this.handleInviteCancel()
        }

      },

      /* 打开 invite 表单 */
      openInvite(){
        this.user_invite = this.default_user_invite;
        this.is_invite_visible=true;
        this.stamp = Date.parse(new Date())

      },

      async onShowSizeChange(current, pageSize) {
        this.current = current
        this.page_size = pageSize
        await this.getUser()
      },

      /* 关闭create */
      handleCancel() {
        this.visible = false;
      },

      /* 创建或者修改 */
      async handleSubmit(user_edit_form) {
        try {

          this.confirmLoading = true;
          if (this.mode === 'Create') {
            await UserService.create(user_edit_form)
          } else {
            user_edit_form['id'] = this.info['id']
            await UserService.update(user_edit_form)
          }
          setTimeout(() => {
            /* 延迟关闭表单 */
            this.getUser()
            this.$message.success(this.mode === 'Create' ? 'Create successfully' : 'Update successfully')
            this.visible = false;
            this.confirmLoading = false;
            this.handleCancel()
          }, 2000);
        }catch{
          this.visible = false;
          this.confirmLoading = false;
          this.handleCancel()
        }
      },

      /* 打开create 表单 */
      openEdit(mode, info=undefined){
        this.mode=mode
        if(this.mode === 'Edit'){
          info.admin = info.admin ? 'true': 'false'
          this.info = info
        }
        else{
          this.info = this.default_info
        }
        this.visible=true
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
        this.query['department'] = this.id;
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
      if (this.did) this.id = this.did;
      else this.id = this.$route.params.did;
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
