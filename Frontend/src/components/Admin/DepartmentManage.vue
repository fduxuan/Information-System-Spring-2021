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

        <a-input v-model="name" placeholder="部门查询" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/>
        <!-- <a-input v-model="email" placeholder="please input email" allow-clear style="width: 200px; margin-right: 20px" @pressEnter="search"/> -->

        <a-tooltip title="搜索">
          <a-button type="primary" shape="circle" icon="search" @click="search"  style="background: #8db2c3; border-color: #8db2c3; margin-right: 20px"/>
        </a-tooltip>
        <a-tooltip title="重置">
          <a-button type="primary" shape="circle" icon="delete" @click="refresh" style="background: #8db2c3; border-color: #8db2c3"/>
        </a-tooltip>

        <a-button type="primary" shape="round" style="margin-left:auto; right: 20px" @click="openEdit('Create')">增加部门</a-button>
      </a-row>
      <a-divider></a-divider>
      <DepartmentEdit :visible="visible"
                :info="info"
                :mode="mode"
                :key="stamp"
                @cancel="handleCancel"
                :confirmLoading="confirmLoading"
                @submit="handleSubmit">

      </DepartmentEdit>
      <a-spin :spinning="loading">
      <a-table  :data-source="users" :pagination="false">


        <!-------------------------- 部门名称--------------------------->
        <a-table-column title="部门名称" key="name">
          <template slot-scope="row">

            <span style="margin-right:5px">{{row.name}}</span>

          </template>
        </a-table-column>

        <!-------------------------- Leader --------------------------->
        <a-table-column title="部门领导" key="leader">
          <template slot-scope="row">
            <UserIcon :user="row.leader_info[0]" type="text"></UserIcon>
          </template>
        </a-table-column>

        <!-------------------------- 编辑 --------------------------->
        <a-table-column title="操作" key="action">
          <template slot-scope="row">
            <!-------------------------- 修改部门信息 --------------------------->
            <a-tooltip placement="top">
                <template slot="title">
                  <span>修改部门信息</span>
                </template>
              <a-icon type="edit" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="openEdit('Edit', row)" />
            </a-tooltip>

            <!-------------------------- 详情 --------------------------->

            <a-tooltip placement="top">
              <template slot="title">
                <span>详情</span>
              </template>
              <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/department/${row.id}`}).catch(e=>{console.log(e)})" />
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
import DepartmentEdit from "@/components/Admin/DepartmentEdit";
// import UserService from "@/models/UserService";
import DepartmentService from "@/models/DepartmentService";
import UserIcon from "@/components/Group/UserIcon";
export default {
    name: "DepartmentManage",
    components:{UserIcon, DepartmentEdit},

    data(){
        return{
          visible: false,
          confirmLoading: false,
          loading: false,
          mode: 'Create',
          default_info: {
            name: "",
            leader: ""
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
            await DepartmentService.create(user_edit_form)
          }
          else{
            user_edit_form['id'] = this.info['id']
            await DepartmentService.update(user_edit_form)
          }

        }catch{
          this.visible = false
          this.handleCancel()
          return
        }
        setTimeout(() => {
          /* 延迟关闭表单 */
          this.getUser()
          this.visible = false;
          // this.confirmLoading = false;
          this.handleCancel()
        }, 2000);

      },

      /* 打开create 表单 */
      openEdit(mode, info=undefined){
        this.mode=mode
        this.stamp = Date.parse(new Date())
        if(this.mode === 'Edit'){
          // info.admin = info.admin ? 'true': 'false'
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
        // if(this.position !== 'all'){
        //   this.query['position'] = this.position
        // }
        if(this.name !== ''){
          this.query['name'] = {"$regex": this.name}
        }
        // if(this.email !== ""){
        //   this.query['email'] = {"$regex": this.email}
        // }
        this.current = 1
        await this.getUser()
      },

      /* 重置搜索，页面等 */
      async refresh(){
        // this.position = 'all'
        this.name = ""
        // this.email = ""
        await this.search()
      },

      async getUser(){
        this.loading = true
        try{
          let index = 0
          let res = await DepartmentService.find({
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
