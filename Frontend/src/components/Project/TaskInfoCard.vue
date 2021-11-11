<!--
   Created on 2021/6/9 9:08 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div v-if="task_info.name !== undefined">
      <a-card class="task-info-card" :title="task_info.name">
        <!-------------------------- 选中任务优先级/详情跳转 --------------------------->
        <a-row slot="extra" type="flex" align="middle">
          <!-- todo: v-class -->
          <a-tag color="red">{{task_info.priority}}</a-tag>
          <a-tooltip placement="top">
              <template slot="title">
                <span>详情</span>
              </template>
              <a-icon type="info-circle" style="font-size: 17px; cursor:pointer; margin-left: 10px;" @click="$router.push({ path:`/taskDetail/${task_info.id}`}).catch(e=>{console.log(e)})" />
          </a-tooltip>
        </a-row>

        <!-------------------------- 选中任务具体描述 --------------------------->
        <a-row style="margin-bottom: 20px">
          <span> {{task_info.description}} </span>

        </a-row>

        <!-------------------------- 任务负责人 --------------------------->
        <a-row style="color: #172b4d; margin-bottom: 20px;" type="flex" align="middle">

            <span style="font-weight: bold; margin-right: 15px">负责人:</span>
            <UserIcon v-if="!input_visible_leader" :user="task_info.leader_info"></UserIcon>

            <a-avatar v-if="!input_visible_leader" @click="input_visible_leader=true; stamp = Date.parse(new Date())" style="background-color:#6e9eb8; cursor: pointer" icon="edit" />

          <!-------------------------- 动态修改负责人 --------------------------->
          <a-row v-else type="flex" align="middle" >
            <UserSelect :key="stamp" @change="(e)=>{new_leader=e.email}"></UserSelect>
            <a-tooltip>
              <template slot="title">
                确认
              </template>
              <a-icon type="check" style="margin-left: 10px; font-size: 20px; color: #0ac356;" @click="changeLeader"/>
            </a-tooltip>
            <a-tooltip>
              <template slot="title">
                取消
              </template>
              <a-icon type="close" style="margin-left: 10px; font-size: 20px; color: #d00f0f;" @click="input_visible_leader=false"/>
            </a-tooltip>
          </a-row>
        </a-row>




        <!-- 查询participation表获得执行人 -->
        <a-row  style="color: #172b4d; margin-bottom: 20px;" type="flex" align="middle">
          <span style="font-weight: bold; margin-right: 15px">执行人:</span>

          <div>
            <span class="task-info-user" v-for="item in task_info.participants" :key="item.email">
              <a-avatar style="background-color:#87d068;"  :src="item.avatar"  />
              <span style="margin-left:5px">{{item.name}}</span>
              <a-popconfirm
                  title="确定删除该执行人？"
                  ok-text="是"
                  cancel-text="否"
                  @confirm="deleteParticipant(item.email)"
              >
                <a-icon type="close-circle" style="position: relative; top: -17px; left: 10px; color: #73736d; cursor: pointer"  />
              </a-popconfirm>
            </span>

          </div>


          <!-------------------------- 动态添加执行人 --------------------------->
          <a-avatar  v-if="!input_visible" @click="input_visible=true; stamp = Date.parse(new Date())" style="background-color:#6e9eb8; cursor: pointer" icon="user-add" />
          <a-row type="flex" align="middle" v-else>
            <UserSelect :key="stamp" @change="(e)=>{new_participant = e.email}"></UserSelect>
            <a-tooltip>
              <template slot="title">
                确认
              </template>
              <a-icon type="check" style="margin-left: 10px; font-size: 20px; color: #0ac356;" @click="addParticipant"/>
            </a-tooltip>
            <a-tooltip>
              <template slot="title">
                取消
              </template>
              <a-icon type="close" style="margin-left: 10px; font-size: 20px; color: #d00f0f;" @click="input_visible=false"/>
            </a-tooltip>
          </a-row>


        </a-row>

        <!-------------------------- 时间和子任务完成度 --------------------------->
        <a-row style="color: #172b4d" type="flex" align="middle">
          <a-col :span="8">
            <span style="font-weight: bold; margin-right: 15px">截止时间:</span>
            <span> {{task_info.end_date}}</span>
          </a-col>

          <a-col :span="8">
            <span style="font-weight: bold; margin-right: 15px">子任务完成度:</span>
            <span class="task-info-user">
              <a-icon type="check-square" style="font-weight: bold; font-size: 15px" /> {{task_info.finish}}/{{task_info.children.length}}
            </span>
          </a-col>

          <a-col :span="8">
            <span style="font-weight: bold; margin-right: 15px">当前状态:</span>
            <a-tag color="purple">{{task_info.status}}</a-tag>
          </a-col>

        </a-row>
      </a-card>

    </div>

</template>

<script>
import PermissionService from "@/models/PermissionService";
import TaskService from "@/models/TaskService";
import UserSelect from "@/components/Admin/UserSelect";
import UserIcon from "@/components/Group/UserIcon";

export default {
    name: "TaskInfoCard",
    components:{
      UserIcon,
      UserSelect

    },
    data(){
        return{
          task_info: {},
          children_finish: 0,
          children_progress: 0,
          input_visible: false,
          input_visible_leader: false,
          new_leader: "",
          new_participant: '',
          stamp: 123,
          is_strict_leader: false,
          is_leader: false,
          is_participant: false
        }
    },
    props: {
      task_id: {
        type: String,
        default() {return ''}
      },
    },

    methods:{
      async getTaskInfo(){
        let task_info = await TaskService.getTaskInfo(this.task_id)
        let finish = 0
        task_info.children.forEach(t=>{
          if (t.status === '已完成'){
            finish += 1
          }
        })
        task_info.finish = finish
        this.task_info = task_info
      },

      /* 添加执行人 */
      async addParticipant(){
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        await TaskService.add_participant(this.task_id, this.new_participant)
        await this.getTaskInfo()
        await this.getPermission()
        this.input_visible = false
      },

      /* 删除执行人 */
      async deleteParticipant(email){
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        await TaskService.remove_participant(this.task_id, email)
        await this.getTaskInfo()
        await this.getPermission()
      },

      /* 修改负责人 */
      async changeLeader(){
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        await TaskService.changeLeader(this.task_id, this.new_leader)
        await this.getTaskInfo()
        await this.getPermission()
        this.input_visible_leader = false
      },

      async getPermission(){
        this.is_strict_leader = await PermissionService.is_strict_leader(this.task_id, this.$store.state.user.email)
        this.is_leader = await PermissionService.is_leader(this.task_id, this.$store.state.user.email)
        this.is_participant = await PermissionService.is_participant(this.task_id, this.$store.state.user.email)
        // console.log("is_strict_leader:", this.is_strict_leader, "is_leader", this.is_leader, "is_participant:", this.is_participant)
      }
    },

    mounted(){
      this.getTaskInfo()
      this.getPermission()
    },
    watch:{
      task_id(newValue){
        this.getTaskInfo(newValue)
        this.getPermission()
      },
    }
}
</script>

<style scoped>
span{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

.task-info-user{
  background:rgba(9, 30, 66, 0.08); padding: 8px 10px; border-radius: 6px;
  margin-right: 10px;
  align-items: center;
  display: inline-block;
}
.task-info-user:hover{
  background:rgba(9, 30, 66, 0.18)
}



</style>
