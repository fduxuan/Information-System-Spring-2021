<!--
   Created on 2021/6/4 8:42 上午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div style="padding: 20px 20px 40px 20px;">
      <a-card class="card-content">
        <!-------------------------- 头部，搜索 --------------------------->
        <ProjectSearch @handleFilterChange="handleFilterChange" @handleProjectCreated="search"></ProjectSearch>
        <a-divider></a-divider>
        <a-spin :spinning="loading">
        <a-table  :data-source="projects" :pagination="false">


          <!-------------------------- 项目id --------------------------->
          <!-- <a-table-column title="项目ID" key="id">
            <template slot-scope="row">
              <a-tag style="margin-right:5px">{{row.id}}</a-tag>
            </template>
          </a-table-column> -->

          <!-------------------------- 项目名称 --------------------------->
          <a-table-column title="项目名称" key="name">
            <template slot-scope="row">
              {{ row.name }}
            </template>
          </a-table-column>

          <!-------------------------- 负责人(创建人) --------------------------->
          <a-table-column title="负责人" key="leader">
            <template slot-scope="row">
              <UserIcon :user="row.leader_info[0]" type="text"></UserIcon>
<!--              <a-avatar style="background-color:#87d068; margin-right: 5px" :src="row.leader_info[0].avatar" />-->
<!--              <span>{{ row.leader }}</span>-->
            </template>
          </a-table-column>

          <!-------------------------- 开始时间 --------------------------->
          <a-table-column title="开始时间" key="start_time">
            <template slot-scope="row">
              {{ row.start_date }}
            </template>
          </a-table-column>

          <!-------------------------- 截止时间 --------------------------->
          <a-table-column title="截止时间" key="end_time">
            <template slot-scope="row">
              {{ row.end_date }}
            </template>
          </a-table-column>

          <!-------------------------- 项目状态 --------------------------->
          <a-table-column title="项目状态" key="end_time">
            <template slot-scope="row">
              <span :class="row.status==='已完成'? 'status-finish': 'status-progress'">{{row.status}}</span>
            </template>
          </a-table-column>

          <!-------------------------- 操作 --------------------------->
          <a-table-column title="操作" key="option">
            <template slot-scope="row">
              <a-tooltip placement="top">
                <template slot="title">
                  <span>详情</span>
                </template>
                <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/projectDetail/${row._id}`}).catch(e=>{console.log(e)})" />
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
      </a-card>
    </div>

</template>

<script>
import ProjectSearch from "@/components/Project/ProjectSearch";
import TaskService from "@/models/TaskService";
import UserIcon from "@/components/Group/UserIcon";
export default {
    name: "Project",
    components:{
      UserIcon,
      ProjectSearch

    },
    data(){
        return{
          projects:[],
          query: {},
          count: 0,
          current: 1,
          page_size: 10,
          loading: false,
          name: "",
          type: "all",
          finished_type: "all",
        }
    },
    props: {

    },

    methods:{
      handleFilterChange(value){

        // filter the projects
        this.type = value['type'];
        this.finished_type = value['finished_type'];
        this.name = value['projectName'];
        this.search();
      },
      async getUser(){
        this.loading = true
        try{
          let index = 0
          let res = await TaskService.find_projects({
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
          this.projects = users


        }finally {
          this.loading = false
        }
      },
      async search(){
        this.query = {}
        // if(this.position !== 'all'){
        //   this.query['position'] = this.position
        // }
        if(this.name !== ''){
          this.query['name'] = {"$regex": this.name}
        }
        if(this.type === 'leader'){
          this.query['leader'] = this.$store.state.user.email
        }
        if (this.finished_type === 'finished'){
          this.query['status'] = '已完成';
        }
        else if (this.finished_type === 'unfinished'){
          this.query['status'] = {'$ne': '已完成'}
        }
        this.current = 1
        await this.getUser()
      },
      async onShowSizeChange(current, pageSize) {
        this.current = current
        this.page_size = pageSize
        await this.getUser()
      },
    },

    mounted(){
      this.getUser();
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

.status-finish{
  padding: 2px 4px 2px 4px;
  border-radius: 4px;
  background: rgba(0, 191, 10, 0.1);
  color: #299f09;
  border: #d5e4da .02em solid

}
.status-progress{
  padding: 2px 4px 2px 4px;
  border-radius: 4px;
  background: rgba(0,127,191,0.1);
  color: #577085;
  border: #d5e4da .02em solid;
}
</style>
