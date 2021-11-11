<template>
  <div style="padding: 20px 20px 40px 20px;">
    <a-modal v-model="is_invite_visible" title="添加执行人"
            okText="添加"
            cancelText="取消"
            @cancel="handleInviteCancel"
            @ok="handleInviteOk"
            :confirm-loading="confirmInviteLoading">
      <a-form-model :model="user_invite" ref="user_invite_form" :rules="user_invite_rules">
        <a-row type="flex" align="middle" justify="space-around">
          <UserSelect @change="(e)=>{user_invite.email=e.email}"></UserSelect>
          <!----------------------- 邮箱 ---------------------->
          <!-- <a-form-model-item label="执行人" prop="email">
            <a-input style="width: 200px" v-model="user_invite.email" placeholder="输入执行人邮箱"></a-input>
          </a-form-model-item> -->
        </a-row>
      </a-form-model>
    </a-modal>
    <a-row>
      <a-col :span="16">
        <a-card class="card-content" title="任务详情" :bordered="false">
          <a-button slot="extra" type="primary" shape="circle" icon="edit" @click="showModifyTaskModal()" />
          <a-button slot="extra" type="primary" shape="circle" icon="user-add" style="margin-left: 5px" @click="openInvite()" />
          <a-descriptions bordered>
            <a-descriptions-item label="名称" :span="2">
              {{currentTask.name}}
            </a-descriptions-item>
            <a-descriptions-item label="优先级">
              {{currentTask.priority}}
            </a-descriptions-item>
            <a-descriptions-item label="开始时间">
              {{currentTask.start_date}}
            </a-descriptions-item>
            <a-descriptions-item label="结束时间">
              {{currentTask.end_date}}
            </a-descriptions-item>
            <a-descriptions-item label="状态" :span="2">
              <a-badge status="processing" :text="currentTask.status" />
            </a-descriptions-item>
            <a-descriptions-item label="任务描述" :span="3">
              {{currentTask.description}}
            </a-descriptions-item>
            <a-descriptions-item label="负责人">
              <!-- <a-tooltip v-if="currentTask.leader_info">
                <template slot="title">
                  {{currentTask.leader_info.name}}
                </template>
                <a-avatar :src="currentTask.leader_info.avatar" />
              </a-tooltip> -->
              <a-tag v-if="currentTask.leader_info">{{currentTask.leader_info.email}}</a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="执行人" :span="2">
              <a-tag v-for="executor in currentTask.participants" :key="executor.id">
                {{executor.email}}
                <a-popconfirm
                  title="确定删除该执行人吗？" ok-text="确定" cancel-text="取消"
                  @confirm="handleRemoveParticipant(executor.email)">
                  <a-icon type="close-circle" style="position: relative; top: 0px; left: 3px; color: #73736d; cursor: pointer" />
                </a-popconfirm>
              </a-tag>
              <!-- <a-tag closable @close="handleRemoveParticipant(executor.email)" v-for="executor in currentTask.participants" :key="executor.id">
                {{executor.email}}
              </a-tag> -->
              <!-- <a-tooltip v-for="executor in currentTask.participants" :key="executor.id">
                <template slot="title">
                  {{executor.name}}
                </template>
                <a-avatar :src="executor.avatar" />
              </a-tooltip> -->
            </a-descriptions-item>
            <a-descriptions-item label="附件" :span="3" v-if="currentTask.attachment">
              {{currentTask.attachment}}
              <a-button shape="circle" icon="eye" />
              <a-button shape="circle" icon="download" />
            </a-descriptions-item>
          </a-descriptions>          
        </a-card>

        <a-card title="子任务" :bordered="false" class="card-content margin_top">
            <a-button slot="extra" type="primary" shape="circle" icon="plus" @click="showCreateTaskModal()" />
            <a-list v-if="currentTask.children && currentTask.children.length>0" item-layout="horizontal" :data-source="currentTask.children">
              <a-list-item slot="renderItem" slot-scope="item">
                <a-list-item-meta>
                  <a slot="title" @click="$router.push({ path:`/taskDetail/${item.id}`}).catch(e=>{console.log(e)})">{{ item.name }} [{{item.status}}]</a>
                  <!-- <template slot="title" class="ant-card-actions"> -->
                    <a-popconfirm slot="title" style="float: right;"
                      title="确定删除这个任务吗？" ok-text="确定" cancel-text="取消"
                      @confirm="handleDeleteTask(item.id)">
                      <a-button type="danger" shape="circle" icon="delete"></a-button>
                    </a-popconfirm>
                  <!-- </template> -->
                </a-list-item-meta>
              </a-list-item>
            </a-list>
            <a-empty v-else />
        </a-card>

      </a-col>
      <a-col :span="8">
        <a-card title="任务执行记录" :bordered="false" class="card-content margin_left">
          <a-button slot="extra" type="primary" shape="circle" icon="edit" @click="showExecutionRecordModal()" />
          <a-steps direction="vertical" v-if="executionRecord.length>0">
            <a-step v-for="record in executionRecord" :key="record.id" status="finish">
              <template slot="title">
                <div style="color:#00adb5;">{{record.text}}</div>
              </template>
              <a-tooltip v-if="record.user_info" slot="icon">
                  <template slot="title">
                    {{record.user_info[0].name}}
                  </template>
                  <a-avatar :src="record.user_info[0].avatar" />
              </a-tooltip>
              
              <template slot="description">
                <!-- <div style="margin-bottom:0.5em;">{{record.text}}</div> -->
                <a-space style="font-size:10px;">
                  <a-icon type="clock-circle" />
                  <span>{{record.datetime}}</span>
                </a-space>
                <br/>
                <a-space style="font-size:10px;">
                  <a-icon type="tag" />
                  <span>{{record.attachment.split('/')[1]}}</span>
                  <a-button icon="download" size="small" style="border-width:0px;" @click="downloadAttachment(record)"/>
                </a-space>
              </template>
            </a-step>
          </a-steps>
          <a-empty v-else />
          

          <template slot="actions" class="ant-card-actions">
            <a-popconfirm v-if="currentTask.status==='进行中'"
              title="确定已经完成这个任务吗？" ok-text="确定" cancel-text="取消"
              @confirm="finishTask()">
              <a-button type="primary">完成</a-button>
            </a-popconfirm>
            <a-button v-if="currentTask.status==='审核中'" type="primary" disabled>审核中</a-button>
            <a-button v-if="currentTask.status==='已完成'" type="primary" disabled>已完成</a-button>
          </template>
        <!-- <a-timeline>
          <a-timeline-item color="green">
            Create a services site 2015-09-01
          </a-timeline-item>
          <a-timeline-item color="green">
            Create a services site 2015-09-01
          </a-timeline-item>
          <a-timeline-item color="red">
            <p>Solve initial network problems 1</p>
            <p>Solve initial network problems 2</p>
            <p>Solve initial network problems 3 2015-09-01</p>
          </a-timeline-item>
        </a-timeline> -->
        </a-card>
      </a-col>
    </a-row>
    <sub-task-create 
      :visible="SubTaskCreateVisible"
      :confirmLoading="SubTaskCreateConfirmLoading"
      :modalType="modalType"
      :modalTitle="modalTitle"
      :currentTask="currentTask"
      :modalForm="modalForm"
      @handleClickOk="handleClickSubTaskCreateOk"
      @handleClickCancel="() => {SubTaskCreateVisible=false; SubTaskCreateConfirmLoading=false;}"
    />

    <execution-record 
      :visible="ExecutionRecordVisible"
      :confirmLoading="ExecutionRecordConfirmLoading"
      @handleClickOk="handleClickExecutionRecordOk"
      @handleClickCancel="ExecutionRecordVisible=false"
    />
  </div>



</template>

<script>
import SubTaskCreate from '../components/Task/SubTaskCreate.vue'
import ExecutionRecord from '../components/Task/ExecutionRecord.vue'
import UserSelect from '@/components/Admin/UserSelect'
import TaskService from '@/models/TaskService'
import CommentService from '@/models/CommentService'
import PermissionService from '@/models/PermissionService'
import moment from "moment"
export default {
    name: "TaskDetail",
    components:{
      SubTaskCreate,
      ExecutionRecord,
      UserSelect
    },
    data(){
        return{
          tid: this.$route.params.tid,
          currentTask: {},
          subtask: [],
          SubTaskCreateVisible: false,
          SubTaskCreateConfirmLoading: false,
          modalForm: {},
          modalType: 'create',
          modalTitle: '创建新任务',
          ExecutionRecordVisible: false,
          ExecutionRecordConfirmLoading: false,
          executionRecord: [],

          is_invite_visible: false,
          confirmInviteLoading: false,
          default_user_invite: {
            email: ""
          },
          user_invite: {
            email: ""
          },
          user_invite_rules: {
            email:[{ required: true, message: "请输入执行人邮箱！", trigger: 'blur' }],
          },

          is_strict_leader: false,
          is_leader: false,
          is_participant: false,
        }
    },
    props: {

    },

    methods:{
      
      async handleRemoveParticipant(user_email) {
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        await TaskService.remove_participant(this.tid, user_email);
        this.getCurrentTask();
        this.getPermission();
        // this.$message.success('移除成功！');
      },

      async handleDeleteTask(task_id) {
        if (!this.is_strict_leader){
          this.$message.error("您不是该任务的负责人，没有权限！")
          return
        }
        await TaskService.deleteTask(task_id);
        this.getCurrentTask();
        this.$message.success('删除成功！');
      },

      /* 关闭create */
      handleInviteCancel() {
        this.is_invite_visible = false;
        this.confirmInviteLoading = false;
      },

      /* 创建或者修改 */
      async handleInviteOk() {
        await this.$refs.user_invite_form.validate();
        this.confirmInviteLoading = true;
        console.log(this.user_invite.email)
        await TaskService.add_participant(this.tid, this.user_invite.email);
        setTimeout(() => {
          /* 延迟关闭表单 */
          this.getCurrentTask();
          this.getPermission();
          // this.$message.success('添加成功！');
          this.handleInviteCancel();
        }, 2000);
      },

      /* 打开 invite 表单 */
      openInvite(){
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        this.user_invite = this.default_user_invite;
        this.is_invite_visible=true;
      },

      async getCurrentTask(){
        this.currentTask = await TaskService.task_info(this.tid)
      },

      async getExecutionRecord(){
        // get execution record using task id
        console.log("getting execution record for task:", this.tid);
        let res = await CommentService.find_comments(this.tid)
        if (res){
          this.executionRecord = res.results
        }
        console.log(this.executionRecord)
        // this.executionRecord = [
        //   {
        //     id: 1,
        //     title: "任务初始化",
        //     description: "创建代码仓库",
        //     executor: {"id": 3, "name": "Yanqi Jiang", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"},
        //     created_at: "2021-06-01",
        //     attachment: "附件1.zip"
        //   },
        //   {
        //     id: 2,
        //     title: "上传demo",
        //     description: "项目基本demo",
        //     executor: {"id": 2, "name": "Xuanjie Fang", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"},
        //     created_at: "2021-06-01",
        //     attachment: "附件2.zip"
        //   }
        // ]
      },

      showCreateTaskModal(){
        if (!this.is_strict_leader){
          this.$message.error("您不是该任务的负责人，没有权限！")
          return
        }
        this.modalType = 'create'
        this.modalTitle = '创建新任务'
        this.modalForm = {}
        this.SubTaskCreateVisible = true
      },

      showModifyTaskModal(){
        if (!this.is_leader){
          this.$message.error("您不是该任务或父任务的负责人，没有权限！")
          return
        }
        this.modalType = 'modify'
        this.modalTitle = '修改任务详情'
        this.modalForm = {
          name: this.currentTask.name,
          priority: this.currentTask.priority,
          start_date: moment(this.currentTask.start_date, 'YYYY-MM-DD'),
          end_date: moment(this.currentTask.end_date, 'YYYY-MM-DD'),
          description: this.currentTask.description,
          leader: this.currentTask.leader_info.email, // select option的value不能接收整个对象
          // executor: this.currentTask.participants.map(obj => {return obj.email;})
        }
        // 防止出现非法日期
        if (this.currentTask.start_date === '0000-00-00'){
          this.modalForm.start_date = null
        }
        if (this.currentTask.end_date === '0000-00-00'){
          this.modalForm.end_date = null
        }
        this.SubTaskCreateVisible = true;
      },

      showExecutionRecordModal(){
        if (!(this.is_participant || this.is_leader)){
          this.$message.error("您不是该任务的负责人或执行人，没有权限！")
          return
        }
        this.ExecutionRecordVisible = true;
      },

      async handleClickSubTaskCreateOk(value){
        value.start_date = value.start_date.format('YYYY-MM-DD');
        value.end_date = value.end_date.format('YYYY-MM-DD');
        // console.log("form data", value)
        this.SubTaskCreateConfirmLoading = true;
        // do something
        if (this.modalType === 'create'){
          // value.root = this.currentTask.root;
          value.parent = this.tid;
          value.position = this.currentTask.children.length + 1;
          await TaskService.createTask(value);
          setTimeout(() => {
            /* 延迟关闭表单 */
            this.getCurrentTask();
            this.SubTaskCreateVisible = false;
            this.SubTaskCreateConfirmLoading = false;
            this.$message.success('添加成功！');
          }, 2000);
        }else{
          value.id = this.tid;
          await TaskService.update(value);
          setTimeout(() => {
            /* 延迟关闭表单 */
            this.getCurrentTask();
            this.SubTaskCreateVisible = false;
            this.SubTaskCreateConfirmLoading = false;
            this.$message.success('更新成功！');
          }, 2000);
        }
      },

      async handleClickExecutionRecordOk(value){
        console.log("form data", value)
        this.ExecutionRecordConfirmLoading = true
        let formData = new FormData()
        const comment_info = {user: this.$store.state.user.email, task: this.currentTask.id, text: value.description}
        console.log(comment_info)
        formData.append("comment_info", JSON.stringify(comment_info))
        formData.append("file", value.file.file)
        formData.append('Content-Type', 'multipart/form-data')
        // console.log("formData", formData.get("comment_info"))
        // console.log(formData.get("file"))
        await CommentService.create_comment(formData)
        this.ExecutionRecordVisible = false
        this.ExecutionRecordConfirmLoading = false
        this.$message.success('新建执行记录成功')
        this.getExecutionRecord()
      },

      async downloadAttachment(comment){
        if (!(this.is_participant || this.is_leader)){
          this.$message.error("您不是该任务的负责人或执行人，没有权限！")
          return
        }
        let resp = await CommentService.download_comment(comment.id)
        console.log(resp.data)
        let blob = new Blob([resp.data], {type: "application/octet-stream"});
        if (window.navigator.msSaveBlob) {
          window.navigator.msSaveBlob(blob, comment.attachment.split('/')[1]);//处理IE下载的兼容性
        } else {
          let downloadElement = document.createElement('a');
          let href = window.URL.createObjectURL(blob); //创建下载的链接
          downloadElement.href = href;
          downloadElement.download =  comment.attachment.split('/')[1] //下载后文件名
          document.body.appendChild(downloadElement);
          downloadElement.click(); //点击下载
          document.body.removeChild(downloadElement); //下载完成移除元素
          window.URL.revokeObjectURL(href); //释放掉blob对象
        }

      },

      async finishTask(){
        // 检测该用户是否为负责人
        // 检测子任务是否都已完成
        // 如果有上一级任务，向上级任务的负责人发送审批信息
        if (!this.is_leader){
          this.$message.error("您不是该任务的负责人，没有权限！")
          return
        }
        await TaskService.update({
          id: this.tid,
          status: '审核中'
        });
        this.$message.success('成功提交请求！');
        this.getCurrentTask();
      },

      async getPermission(){
        this.is_strict_leader = await PermissionService.is_strict_leader(this.tid)
        this.is_leader = await PermissionService.is_leader(this.tid)
        this.is_participant = await PermissionService.is_participant(this.tid)
        console.log("is_strict_leader:", this.is_strict_leader, "is_leader", this.is_leader, "is_participant:", this.is_participant)
      }
    },

    mounted(){
      this.getCurrentTask();
      this.getPermission();
      this.getExecutionRecord();
    },
    watch:{
      $route(){
        this.tid= this.$route.params.tid
      },
      tid(){
        this.getCurrentTask();
        this.getPermission();
        this.getExecutionRecord();
        
      },
    }
}
</script>

<style scoped>
.card-content{
  text-align: left;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  box-shadow:-1px 1px 3px #ACADA3;
}

.margin_top{
  margin-top: 20px;
}

.margin_left{
  margin-left: 20px;
}

.steps-item-description{
  font-size: 12px;
}
</style>
