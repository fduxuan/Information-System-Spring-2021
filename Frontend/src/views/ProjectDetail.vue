<!--
   Created on 2021/6/6 6:50 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
  <div style="padding: 20px 20px 40px 20px;">
    <a-card class="card-content">
      <a-row type="flex" align="middle">
        <span style="font-size: 130%; font-weight: bold">项目详情</span>

        <!-------------------------- 抽屉打开数据图表 --------------------------->
        <a-tooltip>
          <template slot="title">
            数据图表
          </template>
          <a-icon type="bar-chart"  class="project-statistic-icon" @click="openStatistic"/>
        </a-tooltip>

        <a-drawer
            title="项目仪表盘"
            width="100%"
            :visible="draw_visible"
            :body-style="{ paddingBottom: '80px'}"
            @close="draw_visible=false"
        >
          <ProjectGraph v-if="task_statistic.tasks !== undefined" :task_statistic="task_statistic" ></ProjectGraph>
        </a-drawer>
      </a-row>



      <a-divider></a-divider>
      <!-------------------------- 左边wbs树 --------------------------->
      <a-row>
        <a-col :span="5" >
          <ProjectTree :pid="pid" @handleTreeSelect="handleTreeSelect"></ProjectTree>
        </a-col>

        <a-col :span="18" :offset="1">
          <!-------------------------- 右上任务卡片 --------------------------->
          <TaskInfoCard  :task_id="task_id"></TaskInfoCard>
          <br>
          <a-card>
            <!-------------------------- 右下看板 --------------------------->
            <ProjectKanban  :task_id="task_id" @changeStatus="changeStatus"></ProjectKanban>
          </a-card>

        </a-col>
      </a-row>
    </a-card>
  </div>


</template>

<script>
import ProjectTree from "@/components/Project/ProjectTree";
import ProjectKanban from "@/components/Project/ProjectKanban";
import TaskInfoCard from "@/components/Project/TaskInfoCard";
import ProjectGraph from "@/components/Project/ProjectGraph";
import TaskService from "@/models/TaskService";
export default {
    name: "ProjectDetail",
    components:{
      ProjectGraph,
      TaskInfoCard,
      ProjectKanban,
      ProjectTree

    },
    data(){
        return{
          // 顶层项目ID
          pid: this.$route.params.pid,
          // 当前选中的任务ID
          task_id: this.$route.params.pid,
          current_task: {},
          draw_visible: false,
          sub_tasks: [],
          task_statistic: {}
        }
    },
    props: {

    },

    methods:{
      handleTreeSelect(value) {
        this.task_id = value
      },

      changeStatus(task_id){
        console.log('change', task_id)
      },

      /* 获取所有的tasks，非树结构 */
      async getProjectTasks(){
        this.sub_tasks = await TaskService.getTaskStatistic(this.pid)
      },
      async getProjectStatistic(){
        this.task_statistic = await TaskService.getProjectStatistic(this.pid)
        this.task_statistic['pid'] = this.pid
      },

      async openStatistic(){
        this.draw_visible = true
        await this.getProjectStatistic()
      }
    },

    mounted(){
      this.getProjectTasks()
      // this.getProjectStatistic()
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

.project-statistic-icon{
  margin-left: auto;margin-right: 10px; font-size: 30px; color: #123b56;
  cursor: pointer;

}
.project-statistic-icon:hover{
  background: rgba(9, 30, 66, 0.2);

}

</style>
