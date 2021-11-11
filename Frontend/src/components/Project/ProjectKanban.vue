<!--
   Created on 2021/6/9 6:56 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div>
      <!-------------------------- 搜索筛选器 --------------------------->
<!--      <a-row style="margin-left: 10px" type="flex" align="middle">-->
<!--        <a-input-search v-model="search_filters.search_text" style="width: 200px; margin-right: 30px;" size="default" @search="onSearch"></a-input-search>-->
<!--        <span :class="search_filters.my_task ? 'kanban-button-active' : 'kanban-button'" style="margin-right: 20px; " @click="search_filters.my_task=!search_filters.my_task;onSearch();">我的任务</span>-->
<!--        <span :class="search_filters.latest_task ? 'kanban-button-active' : 'kanban-button'" style="margin-right: 20px; " @click="search_filters.latest_task=!search_filters.latest_task;onSearch();"> 本周到期</span>-->
<!--        <span v-if="search_filters.my_task || search_filters.latest_task">-->
<!--          <a-divider type="vertical" style="height: 1.5em; background: #000;margin-right: 20px"></a-divider>-->
<!--          <span style="cursor: pointer" @click="search_filters.latest_task=false; search_filters.my_task=false; search_filters.search_text='';">清除筛选</span>-->
<!--        </span>-->

<!--      </a-row>-->

<!--      <br>-->

      <!-------------------------- 看板组件 --------------------------->
      <kanban-board :stages="stages" :blocks="blocks" :config="config" @update-block="updateBlock" :key="stamp">
        <div v-for="stage in stages" :slot="stage" :key="stage">
          <h2>{{ stage }}</h2>
        </div>

        <div v-for="block in blocks" :slot="block.id" :key="block.id">
          <!-------------------------- 任务名称和优先级tag --------------------------->
          <a-row style="margin-bottom: 20px" type="flex" align="middle">
            <span v-if="block.status === '已完成'"><del>{{block.title}}</del></span>
            <span v-else>{{block.title}}</span>
            <a-tag style="margin-left: auto" :color="block.priority === '高优'? 'red': 'orange'"><strong>{{ block.priority }}</strong></a-tag>
          </a-row>
          <!-------------------------- 任务描述（取前xx字） --------------------------->
          <a-row style="margin-bottom: 20px; font-size: 11px; color: grey">
            {{block.description}}
          </a-row>

          <!-------------------------- 子任务完成度/负责人 --------------------------->
          <a-row  type="flex" align="middle">
            <a-icon v-if="block.status === '已完成'" type="check" style="color: green;margin-right: 2px; font-size: 20px" />
            <a-row style="background:rgba(9, 30, 66, 0.08); font-size: 11px; color: grey; padding: 3px 6px" type="flex" align="middle">
              <a-icon type="check-square" style="font-weight: bold; font-size: 15px; margin-right: 5px" /> {{block.finished}}/{{block.total}}
            </a-row>


            <span style="font-size: 12px; color: grey; margin-left:auto; margin-right: 5px">{{block.end_date}}</span>
            <a-tooltip>
              <template slot="title">
                负责人: {{block.leader_info.name}}
              </template>
            <a-avatar style="background-color:#87d068;"  :src="block.leader_info.avatar" size="small"/>
            </a-tooltip>
          </a-row>


          <br>
        </div>
      </kanban-board>
    </div>

</template>

<script>
import TaskService from "@/models/TaskService";
import PermissionService from "@/models/PermissionService";

export default {
    name: "ProjectKanban",
    components:{

    },
    data(){
        return{
          stages: ['进行中', '审核中', '已完成'],
          stamp: '123',
          blocks: [
            // {
            //   id: 1,
            //   status: '进行中',
            //   title: '一个子任务',
            //   desc:'子任务的描述语句',
            //   end: '06-18',
            //   tag: '中优'
            // },
            // {
            //   id: 2,
            //   status: '进行中',
            //   title: '另一个子任务',
            //   desc:'另一个子任务的描述语句',
            //   tag: '高优',
            //   end: '06-17',
            // },
          ],
          config: {
            // invalid: (el, handle) => {
            //   if (!this.is_leader){
            //     this.$message.error("缺少权限")
            //   }
            //   return !this.is_leader
            // },
          },
          is_strict_leader: false,
          is_leader: false,
          is_participant: false,
          search_filters: {
            search_text: '',
            my_task: false,
            latest_task: false
          }
        }
    },
    props: {
      task_id: {
        type: String,
        default() {return ''}
      },
    },

    methods:{
      async updateBlock(id, status){

        try{
          await TaskService.changeStatus(id, status)
          this.blocks.find(b => b.id === id).status = status
          this.$emit('changeStatus', id)
        }catch{
          await this.getBlocks(this.task_id)

        }
        // let res =
        // console.log(res, res!=="Permission denied")
        // if (res !== "Permission denied"){
        //   console.log("可以更新")
        //   console.log(this.blocks.find(b => b.id === id).status)
        //
        // }

      },
      async getBlocks(task_id){
        this.stamp = Date.parse(new Date())
        let blocks = (await TaskService.getTaskInfo(task_id))['children']
        this.blocks = blocks
        console.log(blocks,'blocks')
      },

      onSearch(){
        console.log("search filters:", this.search_filters)
        // do something
      },

      async getPermission(){
        this.is_strict_leader = await PermissionService.is_strict_leader(this.task_id)
        this.is_leader = await PermissionService.is_leader(this.task_id)
        this.is_participant = await PermissionService.is_participant(this.task_id)
        // console.log("is_strict_leader:", this.is_strict_leader, "is_leader", this.is_leader, "is_participant:", this.is_participant)
      }


    },

    async mounted(){
      this.getBlocks(this.task_id)
      // 避免重复请求API，对每个task先做一个全局的权限判断
      this.getPermission()
    },

    watch:{
      async task_id(newValue){
        this.getBlocks(newValue)
        this.getPermission()
      },
    }
}
</script>

<style scoped>

>>>.drag-column{
  background: #eaf0f1;
}

>>>.drag-item{
  background: #fff;
  height: 130px;
  box-shadow: 0 0 1px #ACADA3;
  border-radius: 4px;
  cursor: pointer;
}

>>>.drag-item:hover{
  box-shadow:-1px 1px 3px #ACADA3;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  background: #fafafa;
}

>>>.drag-inner-list{
  color: #172b4d;
  font-size: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  font-weight: bolder;
}

.kanban-button{
  background: rgba(9, 30, 66, 0.1);
  padding:  6px 10px;
  font-size: 13px;
  color: #172b4d;
  font-weight: bold;
  cursor: pointer;
  border-radius: 2px;
}

.kanban-button-active{
  background: rgb(37, 56, 88);
  padding:  6px 10px;
  font-size: 13px;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  border-radius: 2px;
}
</style>
