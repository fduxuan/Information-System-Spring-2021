<!--
   Created on 2021/6/7 9:35 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div style="border: 1px solid #e8e8e8; overflow-x: scroll">
      <a-tree v-if="project_info.key !== undefined" show-line
        :tree-data="[project_info]"
        :show-icon="true"
        :selectedKeys="selected_node"
        :defaultExpandedKeys="[pid]"
      >
        <template slot="custom" slot-scope="item">
          <a-row type="flex" align="middle">
            <span class="title" style="margin-right: 30px" @click="selectNode(item)">{{ item.title }}</span>
            <!-------------------------- 增加删除节点 --------------------------->
            <a-icon v-if="selected_node[0] === item.id" type="plus-circle" @click="openCreate(item)"  style="margin-right: 10px; font-size: 16px; cursor: pointer; z-index:200" />
            <a-popconfirm
                title="是否要删除该任务？"
                ok-text="删除"
                cancel-text="取消"
                @confirm="deleteTask(item.id)"
            >
              <a-icon v-if="selected_node[0] === item.id && item.id !== pid" type="delete"  style="font-size: 16px; cursor: pointer; "/>
            </a-popconfirm>
          </a-row>

        </template>
      </a-tree>

      <!-------------------------- 简单增加节点，只填写名称描述和位置，责任人默认为创建者 --------------------------->
      <a-modal v-model="visible" title="创建子任务" @ok="handleCreate" width="400px" okText="创建" cancelText="取消">
        <a-row type="flex" align="middle" style="margin-bottom: 20px; font-weight: bold">
          <a-col :span="6"> 任务名称: </a-col>
          <a-col :span="14" :offset="2"><a-input placeholder="请填写任务名称" v-model="create_form.name"></a-input></a-col>
        </a-row>
        <a-row type="flex" align="middle" style="margin-bottom: 20px; font-weight: bold">
          <a-col :span="6"> 任务描述: </a-col>
          <a-col :span="14" :offset="2">
            <a-textarea placeholder="请填写任务描述" v-model="create_form.description" :auto-size="{ minRows: 2, maxRows: 6 }"/>
          </a-col>
        </a-row>

        <a-row type="flex" align="top" style="font-weight: bold">
          <a-col :span="6"> 任务位置:<br>  <span style="color: #868585; font-size: 80%">对应任务之后</span></a-col>
          <a-col :span="14" :offset="2">

            <a-select :key="current_task.stamp"  default-value="首位" style="width: 205px" @change="handleChangePosition">
              <a-select-option v-for="(child, index) in current_child" :key="index+1" :value="index+1">
                {{child.name}}
              </a-select-option>
            </a-select><br>
          </a-col>
        </a-row>
      </a-modal>



    </div>

</template>

<script>
import TaskService from "@/models/TaskService";
// import moment from "moment";
import PermissioService from "@/models/PermissionService"

export default {
    name: "ProjectTree",
    components:{

    },
    data(){
        return {
          tree_data: [],
          project_info: {},
          selected_node: [],
          visible: false,
          current_task: {},
          current_child: [],
          position_value: '首位',
          create_form: {
            'name': '',
            'description': '',
            'position': 1
          }
        }
    },
    props: {
      pid: {
        type: String,
        default() {return ''}
      },
    },

    methods:{
      async getProjectTree(pid){
        this.project_info = await TaskService.project_info(pid)
        this.selected_node = [pid]

        this.$emit('handleTreeSelect', pid)
      },

      selectNode(currentTask){
        this.selected_node = [currentTask.id]
        this.$emit('handleTreeSelect', currentTask.id)
      },



      /* 打开表单。默认首位 */
      async openCreate(current_task){
        if (!await PermissioService.is_strict_leader(current_task.id)){
          this.$message.error("您不是该任务的负责人，没有权限！")
          return
        }
        this.visible=true
        current_task.stamp = Date.parse(new Date())
        this.current_task = current_task
        this.position_value = '首位'
        let current_child = current_task.children.slice()
        current_child.unshift( {name: '首位', id: 'shouwei'})
        current_child.push({name: '末位', id: 'mowei'})
        this.current_child = current_child
      },

      /* 简单创建 */
      async handleCreate(){
        if(this.create_form.description === '' || this.create_form.name === ''){
          this.$message.error('请填写完整表单')
        }
        else{
          this.create_form.root = this.pid
          this.create_form.parent = this.current_task.id
          this.create_form.leader = this.$store.state.user.email

          await TaskService.createTask(this.create_form)
          this.create_form = {'name': '', 'description': '', 'position': 1}
          await this.getProjectTree(this.pid);
          this.$message.success('创建成功!')
          this.visible = false
        }

      },


      handleChangePosition(index) {
        this.create_form.position=index
      },

      /* 删除任务 */
      async deleteTask(task_id){
        if (!await PermissioService.is_strict_leader(task_id)){
          this.$message.error("您不是该任务的负责人，没有权限！")
          return
        }
        await TaskService.deleteTask(task_id)
        await this.getProjectTree(this.pid)
        this.$message.success('成功删除！')
      }

    },

    mounted(){
      this.getProjectTree(this.pid);
    },
}
</script>

<style scoped>
>>>.ant-tree li .ant-tree-node-content-wrapper{
  background: #ffffff;
}
>>>.ant-tree li .ant-tree-node-content-wrapper .title {
  color: #5d5a5a;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  font-size: 15px;
  font-weight: bold;
  background: rgba(9, 30, 66, 0.1);
  border: 1px solid #d9d9d9;
  padding: 0 5px 0 5px
}

>>>.ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected .title{
  background: rgb(69, 80, 100);
  color: #fff;
  font-weight: bold;
  border: 1px solid #d9d9d9;
  padding: 0 5px 0 5px
}

>>>.ant-tree-switcher{
  font-size: 15px;
}

</style>
