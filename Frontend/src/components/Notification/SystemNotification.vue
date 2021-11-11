<template>
  <a-list item-layout="vertical" :data-source="notifications">
    <a-list-item slot="renderItem" slot-scope="item" class="no-border-list">
      <!-------------------- 标题为 来自xxx（任务负责人）的审批请求，关于xxx任务 ------------------->
      <a-card class="notification-card"
              :headStyle="headStyle"
              v-if="item.type===0"
              :title="'来自 '+item.target_user_info[0].name+' 关于 '+item.task_info[0].name+' 的审批回复'">
        <span slot="extra" style="font-size: 50%">{{ item.submitted_datetime }}</span>
        <a-row>
          <!-------------------- 左三分之一为请求者（任务负责人）信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">审批人信息</p>
            <p>姓名: {{item.target_user_info[0].name}}</p>
            <p>Email: {{item.target_user_info[0].email}}</p>
          </a-col>
          <!-------------------- 中三分之一为任务信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">
                任务信息
                <a-tooltip placement="top">
                    <template slot="title">
                    <span>详情</span>
                    </template>
                    <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/taskDetail/${item.task_info[0]._id}`}).catch(e=>{console.log(e)})" />
                </a-tooltip>
            </p>
            <p>名称: {{item.task_info[0].name}}</p>
            <p>内容: {{item.task_info[0].description}}</p>
          </a-col>
          <!-------------------- 右三分之一为操作 ------------------->
          <a-col :span="7" :offset="1">
            <p class="notification-title">操作</p>
            <br>
            <!-------------------- 已经操作的invitation ------------------->
            <a-row>
              <a-button :disabled="true" class="notification-button">{{get_approval_status(item.status)}}</a-button>
            </a-row>
          </a-col>

        </a-row>
      </a-card>
      <!-------------------- 标题为 来自xxx（任务负责人）的邀请，关于xxx任务 ------------------->
      <a-card class="notification-card"
              :headStyle=headStyle
              v-else
              :title="'来自 '+item.target_user_info[0].name+' 关于参与任务 '+item.task_info[0].name+' 的回复'">
        <span slot="extra" style="font-size: 50%">{{ item.submitted_datetime }}</span>
        <a-row>
          <!-------------------- 左三分之一为邀请者（任务负责人）信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">邀请人信息</p>
            <p>姓名: {{item.target_user_info[0].name}}</p>
            <p>Email: {{item.target_user_info[0].email}}</p>
          </a-col>
          <!-------------------- 中三分之一为任务信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">
              任务信息
              <a-tooltip placement="top">
                <template slot="title">
                <span>详情</span>
                </template>
                <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/taskDetail/${item.task_info[0]._id}`}).catch(e=>{console.log(e)})" />
              </a-tooltip>
            </p>
            <p>名称: {{item.task_info[0].name}}</p>
            <p>内容: {{item.task_info[0].description}}</p>
          </a-col>
          <!-------------------- 右三分之一为操作 ------------------->
          <a-col :span="7" :offset="1">
            <p class="notification-title">回复</p>
            <br>
            <!-------------------- 已经操作的invitation ------------------->
            <a-row>
              <a-button :disabled="true" class="notification-button">{{get_invitation_status(item.status)}}</a-button>
            </a-row>
          </a-col>

        </a-row>
      </a-card>
    </a-list-item>
  </a-list>

</template>

<script>
// import NotificationService from "@/models/NotificationService";
export default {
    name: "SystemNotification",
    components:{

    },
    props: {
      notifications: {
        type: Array,
        default() {return []}
      }
    },
    data(){
        return{
          headStyle: { fontSize: "150%", color: "#060930", backgroundColor: 'rgba(234, 240, 241, 0.7)' }
        }
    },

    methods:{

      /* 将通知标为已读或者未读 */
      // async markReadOrUnread(nid, index, status){
      //   await NotificationService.changeNotificationStatus(nid, status)
      //   this.$message.success(`success mark this notification to ${status}!`)
      //   this.$emit('handleNotiChange', index)
      // },

      get_invitation_status(status) {
        if (status === 1) return '已接受';
        else if (status === -1) return '已拒绝';
        return undefined;
      },

      get_approval_status(status) {
        if (status === 1) return '已通过';
        else if (status === -1) return '已拒绝';
        return undefined;
      },

    }
}
</script>

<style scoped>
.notification-card{
  border-radius: 4px;
  text-align: left;
}

.notification-title{
  font-weight: bold;
  font-size: 110%;
  color:#16697a;
}
.notification-button{
  font-weight: bold;
}

.ant-list-split .no-border-list.ant-list-item {
  border-bottom: none;
}
</style>
